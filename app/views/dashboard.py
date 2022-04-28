#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.views.generic.list import ListView

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy, reverse

from app.models import Pedido, FormaPagamento, Vendedor, Cliente
from app.mixins import PedidoMixin

from django_datatables_view.base_datatable_view import BaseDatatableView

import django_filters


class PedidoFilter(django_filters.FilterSet):
    data_inicial = django_filters.DateFilter(
        field_name='criado_em',
        lookup_expr='gte',
        label='Data Inicial',
    )
    data_final = django_filters.DateFilter(
        field_name='criado_em',
        lookup_expr='lte',
        label='Data Final',
    )
    forma_pagamento = django_filters.ModelChoiceFilter(
        field_name='forma_pagamento__tipo',
        lookup_expr='icontains',
        label='Forma de Pagamento',
        queryset=FormaPagamento.objects.all(),
    )
    cliente = django_filters.CharFilter(
        field_name='cliente__nome',
        lookup_expr='icontains',
        label='Nome do Cliente',
    )
    vendedor = django_filters.ModelChoiceFilter(
        field_name='vendedor',
        lookup_expr='exact',
        label='Vendedor',
        queryset=Vendedor.objects.all(),
    )

    class Meta:
        model = Pedido
        fields = {
            'valor_total': ['lte', 'gte'],
        }


class DashboardView(LoginRequiredMixin, PedidoMixin, ListView):
    """
    List all Pedidos
    """
    login_url = '/admin/login/'
    template_name = 'dashboard/list.html'
    model = Pedido
    context_object_name = 'pedidos'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = PedidoFilter(self.request.GET, queryset)
        context["filter"] = filter
        return context


class DashboardListJson(BaseDatatableView):
    model = Pedido
    columns = ("id", "cliente", "forma_pagamento", "valor_total", "vendedor", "status", "criado_em", "alterado_em")
    order_columns = ["id", "cliente", "forma_pagamento", "valor_total", "vendedor", "status", "criado_em"]
    max_display_length = 500

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'criado_em':
            # escape HTML for security reasons
            return row.criado_em.strftime("%d-%m-%Y %H:%M:%S")
        else:
            return super(DashboardListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(id__icontains=search) | Q(vendedor__id__icontains=search) | Q(cliente__nome__icontains=search) | Q(
                    forma_pagamento__tipo__icontains=search) | Q(status__nome_status__icontains=search) | Q(
                    valor_total__icontains=search))
        filter = PedidoFilter(self.request.GET, qs)
        return filter.qs


class ClienteFilter(django_filters.FilterSet):
    data_inicial = django_filters.DateFilter(
        field_name='criado_em',
        lookup_expr='gte',
        label='Data Inicial',
    )
    data_final = django_filters.DateFilter(
        field_name='criado_em',
        lookup_expr='lte',
        label='Data Final',
    )
    nome = django_filters.DateFilter(
        field_name='nome',
        lookup_expr='icontains',
        label='Nome',
    )

    class Meta:
        model = Cliente
        fields = ['tipo', ]


class TopClientesView(LoginRequiredMixin, PedidoMixin, ListView):
    """
    List all Pedidos
    """
    login_url = '/admin/login/'
    template_name = 'dashboard/top_clientes.html'
    model = Cliente
    context_object_name = 'clientes'
