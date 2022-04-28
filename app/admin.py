#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from app.models import *


# Register your models here.


class PedidoInline(admin.TabularInline):
    model = Pedido


class ClienteAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = [PedidoInline]
    list_display = (
        "id", "nome", "telefone", "cpf", "cnpj", "email", "instagram", "tipo")


admin.site.register(Cliente, ClienteAdmin)


class VendedorAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = [PedidoInline]
    list_display = ("id", "user")


admin.site.register(Vendedor, VendedorAdmin)


class FormaPagamentoAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = [PedidoInline]
    list_display = ("id", "tipo")


admin.site.register(FormaPagamento, FormaPagamentoAdmin)


class StatusPedidoAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = [PedidoInline]
    list_display = ("id", "nome_status", "cor")


admin.site.register(StatusPedido, StatusPedidoAdmin)


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido


class PedidoAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = [ItemPedidoInline]
    list_display = ("id", "vendedor", "cliente", "forma_pagamento", "status", "valor_total")


admin.site.register(Pedido, PedidoAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = [ItemPedidoInline]
    list_display = ("id", "descricao", "preco_custo", "valor_unitario", "foto")


admin.site.register(Item, ItemAdmin)


class ItemPedidoAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = []
    list_display = ("id", "pedido", "qtd", "item", "valor_total")


admin.site.register(ItemPedido, ItemPedidoAdmin)


class ItemOrcamentoInline(admin.TabularInline):
    model = ItemOrcamento


class OrcamentoAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = [ItemOrcamentoInline]
    list_display = ("id", "vendedor", "cliente", "forma_pagamento", "valor_total")


admin.site.register(Orcamento, OrcamentoAdmin)


class ItemOrcamentoAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = []
    list_display = ("id", "orcamento", "qtd", "item", "valor_total")

admin.site.register(ItemOrcamento, ItemOrcamentoAdmin)
