# estoque/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produto/<int:produto_id>/', views.detalhes_produto, name='detalhes_produto'),
    path('registrar-venda/', views.registrar_venda, name='registrar_venda'),
    path('vendas/', views.lista_vendas, name='lista_vendas'),
    path('caixa/', views.caixa, name='caixa'),  

]
