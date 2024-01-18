# estoque/admin.py

from django.contrib import admin
from .models import Categoria, Produto, Venda, ItemVenda

class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1  # Número de formulários vazios para exibição

class VendaAdmin(admin.ModelAdmin):
    inlines = [ItemVendaInline]

admin.site.register(Venda, VendaAdmin)

admin.site.register(Categoria)
admin.site.register(Produto)