# estoque/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Produto, TransacaoEstoque, Venda, ItemVenda
# estoque/views.py
from django.db.models import Sum

def caixa(request):
    vendas = Venda.objects.all()
    total_caixa = Venda.objects.filter(status='pago').aggregate(total_caixa=Sum('valor_pago'))['total_caixa'] or 0
    total_a_receber = Venda.objects.filter(status__in=['nao_pago', 'parcialmente_pago']).aggregate(total_a_receber=Sum('valor_total') - Sum('valor_pago'))['total_a_receber'] or 0
    return render(request, 'estoque/caixa.html', {'vendas': vendas, 'total_caixa': total_caixa, 'total_a_receber': total_a_receber})

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/lista_produtos.html', {'produtos': produtos})

def detalhes_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    transacoes = TransacaoEstoque.objects.filter(produto=produto)
    return render(request, 'estoque/detalhes_produto.html', {'produto': produto, 'transacoes': transacoes})

def registrar_venda(request):
    if request.method == 'POST':
        produtos_ids = request.POST.getlist('produtos')
        valor_pago = float(request.POST['valor_pago']) if request.POST['valor_pago'] else 0.0

        venda = Venda(
            descricao=request.POST['descricao'],
            cliente_nome=request.POST['cliente_nome'],
            usuario=request.user,
            valor_total=0,
            status='nao_pago',
            valor_pago=valor_pago
        )
        venda.save()

        for produto_id in produtos_ids:
            quantidade = request.POST.get(f'quantidade_{produto_id}')

            produto = get_object_or_404(Produto, pk=produto_id)

            # Verifica se há estoque suficiente para realizar a venda
            if produto.quantidade_estoque >= int(quantidade):
                item_venda = ItemVenda(
                    venda=venda,
                    produto=produto,
                    quantidade=quantidade,
                    subtotal=produto.preco_venda * int(quantidade)
                )
                item_venda.save()

                # Subtrai a quantidade vendida do estoque
                produto.quantidade_estoque -= int(quantidade)
                produto.save()
            else:
                return render(request, 'estoque/registrar_venda.html', {'produtos': Produto.objects.all(), 'erro_estoque': True})

        # Lógica para calcular o valor total da venda e atualizar o registro de venda
        venda.valor_total = sum(item.subtotal for item in venda.itemvenda_set.all())
        venda.save()

        # Lógica para definir o status da venda com base no valor pago
        if valor_pago == venda.valor_total:
            venda.status = 'pago'
        elif valor_pago > 0:
            venda.status = 'parcialmente_pago'
        
        venda.save()

        return redirect('lista_vendas')
    else:
        produtos = Produto.objects.all()
        erro_estoque = request.GET.get('erro_estoque', False)
        return render(request, 'estoque/registrar_venda.html', {'produtos': produtos, 'erro_estoque': erro_estoque})


def lista_vendas(request):
    vendas = Venda.objects.all()
    return render(request, 'estoque/lista_vendas.html', {'vendas': vendas})
