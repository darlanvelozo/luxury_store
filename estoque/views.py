# estoque/views.py
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from .models import Produto, TransacaoEstoque, Venda, ItemVenda
# estoque/views.py
from django.db.models import Sum
from django.db.models import Sum, F
from django.db import transaction

def caixa(request):
    vendas = Venda.objects.all()
    lucro_total = Decimal(0)
    lucro_em_caixa = Decimal(0)
    # Cálculo do Lucro Total
    for produto in Produto.objects.all():
        lucro_total += (produto.preco_venda - produto.preco_custo) * produto.quantidade_estoque

    # Cálculo do Lucro em Caixa
    for venda in vendas:
        for item_venda in venda.itemvenda_set.all():
            lucro_em_caixa += (item_venda.produto.preco_venda - item_venda.produto.preco_custo) * item_venda.quantidade
    total_caixa = Venda.objects.aggregate(total_caixa=Sum('valor_pago'))['total_caixa'] or 0
    total_a_receber = Venda.objects.filter(status__in=['nao_pago', 'parcialmente_pago']).aggregate(total_a_receber=Sum('valor_total') - Sum('valor_pago'))['total_a_receber'] or 0
    context = {
        'vendas': vendas,
        'total_caixa': total_caixa,
        'total_a_receber': total_a_receber,
        'lucro_total': lucro_total,
        'lucro_em_caixa': lucro_em_caixa,
    }

    return render(request, 'estoque/caixa.html', context)
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/lista_produtos.html', {'produtos': produtos})

def detalhes_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    transacoes = TransacaoEstoque.objects.filter(produto=produto)
    return render(request, 'estoque/detalhes_produto.html', {'produto': produto, 'transacoes': transacoes})

@transaction.atomic
def registrar_venda(request):
    if request.method == 'POST':
        print("Dados do formulário:")
        print("Dados do formulário:", request.POST.dict())
        
        produtos_ids = request.POST.getlist('produtos_selecionados')
        valor_pago = Decimal(request.POST.get('valor_pago', 0.0))

        venda = Venda(
            descricao=request.POST['descricao'],
            cliente_nome=request.POST['cliente_nome'],
            usuario=request.user,
            valor_total=0,
            status='nao_pago',
            valor_pago=valor_pago
        )
        venda.save()

        total_venda = 0

        for produto_id in produtos_ids:
            quantidade = int(request.POST.get(f'quantidade_{produto_id}', 0))
            print(f"Produto ID: {produto_id}, Quantidade: {quantidade}")

            produto = get_object_or_404(Produto, pk=produto_id)
            print(f"Detalhes do Produto: {produto.nome}, Preço: {produto.preco_venda}")

            if produto.quantidade_estoque >= quantidade:
                item_venda = ItemVenda(
                    venda=venda,
                    produto=produto,
                    quantidade=quantidade,
                    subtotal=Decimal(produto.preco_venda) * quantidade
                )
                item_venda.save()

                total_venda += item_venda.subtotal

                produto.quantidade_estoque -= quantidade
                produto.save()
            else:
                print("Entrou na condição de estoque")
                return render(request, 'estoque/registrar_venda.html', {'produtos': Produto.objects.all(), 'erro_estoque': True})

        venda.valor_total = total_venda
        venda.save()

        if valor_pago == venda.valor_total:
            venda.status = 'pago'
        elif valor_pago > 0:
            venda.status = 'parcialmente_pago'

        venda.save()

        print("Venda salva com sucesso")

        return redirect('lista_vendas')
    else:
        produtos = Produto.objects.all()
        erro_estoque = request.GET.get('erro_estoque', False)
        return render(request, 'estoque/registrar_venda.html', {'produtos': produtos, 'erro_estoque': erro_estoque})



def lista_vendas(request):
    vendas = Venda.objects.all()
    return render(request, 'estoque/lista_vendas.html', {'vendas': vendas})
