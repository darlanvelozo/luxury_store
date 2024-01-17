# estoque/models.py
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
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Certifique-se de importar User do django.contrib.auth.models
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_hora = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pago', 'Pago'), ('parcialmente_pago', 'Parcialmente Pago'), ('nao_pago', 'Não Pago')])
    def __str__(self):
        return self.cliente_nome
class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
