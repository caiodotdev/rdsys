#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, DeleteView, UpdateView
)
from django.views.generic.list import ListView

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy, reverse

from app.models import Pedido, StatusPedido
from app.forms import PedidoForm, ItemPedidoPedidoFormSet, ItemPedidoPedidoUpdateFormSet
from app.mixins import PedidoMixin
from app.conf import PEDIDO_DETAIL_URL_NAME, PEDIDO_LIST_URL_NAME

from django_datatables_view.base_datatable_view import BaseDatatableView

import django_filters


class PedidoFormSetManagement(object):
    formsets = [ItemPedidoPedidoFormSet]

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            self.object = form.save()

            for Formset in self.formsets:
                formset = context["{}set".format(str(Formset.model.__name__).lower())]
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()
        return super(PedidoFormSetManagement, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(PedidoFormSetManagement, self).get_context_data(**kwargs)
        for Formset in self.formsets:
            if self.request.POST:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(self.request.POST,
                                                                                    self.request.FILES,
                                                                                    instance=self.object)
            else:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(instance=self.object)
        return data


class PedidoUpdateFormSetManagement(PedidoFormSetManagement):
    formsets = [ItemPedidoPedidoUpdateFormSet]


class PedidoFilter(django_filters.FilterSet):
    class Meta:
        model = Pedido
        fields = ["id", "vendedor__id", "cliente__nome", "forma_pagamento__tipo", "status__nome_status", "valor_total"]


class List(LoginRequiredMixin, PedidoMixin, ListView):
    """
    List all Pedidos
    """
    login_url = '/admin/login/'
    template_name = 'pedido/list.html'
    model = Pedido
    context_object_name = 'pedidos'
    paginate_by = 1

    def get_queryset(self):
        today = datetime.datetime.now()
        return self.model.objects.filter(criado_em__month=today.month,
                                         criado_em__year=today.year)

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = PedidoFilter(self.request.GET, queryset)
        context["filter"] = filter
        today = datetime.datetime.now()
        context['abertos'] = Pedido.objects.filter(status=StatusPedido.objects.get(nome_status='Aberto'),
                                                   criado_em__year=today.year,
                                                   criado_em__month=today.month).count()
        context['producao'] = Pedido.objects.filter(status=StatusPedido.objects.get(nome_status='Em Produção'),
                                                    criado_em__year=today.year,
                                                    criado_em__month=today.month).count()
        context['finalizados'] = Pedido.objects.filter(
            status=StatusPedido.objects.get(nome_status='Finalizado'),
            criado_em__year=today.year,
            criado_em__month=today.month).count()
        context['pedidos_mes'] = self.get_queryset().count()
        return context


class ListFull(LoginRequiredMixin, PedidoMixin, ListView):
    """
    List all Pedidos
    """
    login_url = '/admin/login/'
    template_name = 'pedido/list_full.html'
    model = Pedido
    context_object_name = 'pedidos'
    ordering = '-id'
    paginate_by = 10
    search = ''

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = PedidoFilter(self.request.GET, queryset)
        queryset = self.search_general(filter.qs)
        queryset = self.ordering_data(queryset)
        return queryset

    def search_general(self, qs):
        if 'search' in self.request.GET:
            self.search = self.request.GET['search']
            if self.search:
                search = self.search
                qs = qs.filter(Q(id__icontains=search) | Q(vendedor__id__icontains=search) | Q(
                    cliente__nome__icontains=search) | Q(forma_pagamento__tipo__icontains=search) | Q(
                    status__nome_status__icontains=search) | Q(valor_total__icontains=search))
        return qs

    def get_ordering(self):
        if 'ordering' in self.request.GET:
            self.ordering = self.request.GET['ordering']
            if self.ordering:
                return self.ordering
            else:
                self.ordering = '-id'
        return self.ordering

    def ordering_data(self, qs):
        qs = qs.order_by(self.get_ordering())
        return qs

    def get_context_data(self, **kwargs):
        context = super(ListFull, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = PedidoFilter(self.request.GET, queryset)
        page_size = self.get_paginate_by(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context.update(**{
                'ordering': self.ordering,
                'search': self.search,
                'filter': filter,
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset
            })
        else:
            context.update(**{
                'search': self.search,
                'ordering': self.ordering,
                'filter': filter,
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset
            })
        return context


class Create(LoginRequiredMixin, PedidoMixin, PermissionRequiredMixin, PedidoFormSetManagement, CreateView):
    """
    Create a Pedido
    """
    login_url = '/admin/login/'
    model = Pedido
    permission_required = (
        'app.add_pedido'
    )
    form_class = PedidoForm
    template_name = 'pedido/create.html'
    context_object_name = 'pedido'

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy(PEDIDO_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_initial(self):
        data = super(Create, self).get_initial()
        data['vendedor'] = self.request.user.vendedor_set.first()
        return data

    def form_valid(self, form):
        cliente = form.cleaned_data['cliente']
        num_pedidos_cliente = cliente.pedido_set.all().count()
        if num_pedidos_cliente >= 1:
            cliente.tipo = 'Normal'
            cliente.save()
        messages.success(self.request, 'Pedido criado com sucesso')
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Create, self).form_invalid(form)


class Detail(LoginRequiredMixin, PedidoMixin, DetailView):
    """
    Detail of a Pedido
    """
    login_url = '/admin/login/'
    model = Pedido
    template_name = 'pedido/detail.html'
    context_object_name = 'pedido'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        return context


class Update(LoginRequiredMixin, PedidoMixin, PermissionRequiredMixin, PedidoUpdateFormSetManagement, UpdateView):
    """
    Update a Pedido
    """
    login_url = '/admin/login/'
    model = Pedido
    template_name = 'pedido/update.html'
    context_object_name = 'pedido'
    form_class = PedidoForm
    permission_required = (
        'app.change_pedido'
    )

    def get_initial(self):
        data = super(Update, self).get_initial()
        return data

    def get_success_url(self):
        return reverse_lazy(PEDIDO_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_context_data(self, **kwargs):
        data = super(Update, self).get_context_data(**kwargs)
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Pedido atualizado com sucesso')
        return super(Update, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Update, self).form_invalid(form)


class Delete(LoginRequiredMixin, PedidoMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete a Pedido
    """
    login_url = '/admin/login/'
    model = Pedido
    permission_required = (
        'app.delete_pedido'
    )
    template_name = 'pedido/delete.html'
    context_object_name = 'pedido'

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        collector = NestedObjects(using='default')
        collector.collect([self.get_object()])
        context['deleted_objects'] = collector.nested()
        return context

    def __init__(self):
        super(Delete, self).__init__()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Pedido removido com sucesso')
        return super(Delete, self).delete(self.request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(PEDIDO_LIST_URL_NAME)


class PedidoListJson(BaseDatatableView):
    model = Pedido
    columns = ("id", "cliente", "forma_pagamento", "valor_total", "vendedor", "criado_em", "status", "alterado_em")
    order_columns = ["id", "cliente", "forma_pagamento", "valor_total", "vendedor", "criado_em", "status"]
    max_display_length = 500

    def get_initial_queryset(self):
        today = datetime.datetime.now()
        return self.model.objects.filter(criado_em__month=today.month,
                                         criado_em__year=today.year)

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'criado_em':
            # escape HTML for security reasons
            return row.criado_em.strftime("%d-%m-%Y %H:%M:%S")
        else:
            return super(PedidoListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(id__icontains=search) | Q(vendedor__id__icontains=search) | Q(cliente__nome__icontains=search) | Q(
                    forma_pagamento__tipo__icontains=search) | Q(status__nome_status__icontains=search) | Q(
                    valor_total__icontains=search))
        filter = PedidoFilter(self.request.GET, qs)
        return filter.qs
