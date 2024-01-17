# estoque/admin.py

from django.contrib import admin
from .models import Categoria, Produto, Venda

admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Venda)