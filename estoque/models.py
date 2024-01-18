# estoque/models.py
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = models.IntegerField()
    def __str__(self):
        return self.nome

class TransacaoEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('saida', 'Saída')])
    data = models.DateTimeField(auto_now_add=True)

class Venda(models.Model):
    descricao = models.TextField()
    cliente_nome = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_hora = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pago', 'Pago'), ('parcialmente_pago', 'Parcialmente Pago'), ('nao_pago', 'Não Pago')])

    def save(self, *args, **kwargs):
        # Atualizar o valor_total antes de salvar
        self.valor_total = sum(item.subtotal for item in self.itemvenda_set.all())
        super().save(*args, **kwargs)


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Atualizar o subtotal antes de salvar
        self.subtotal = Decimal(self.produto.preco_venda) * self.quantidade
        super().save(*args, **kwargs)
