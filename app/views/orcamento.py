#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, DeleteView, UpdateView
)
from django.views.generic.list import ListView

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy, reverse

from app.models import Orcamento, Pedido, ItemPedido, StatusPedido
from app.forms import OrcamentoForm, ItemOrcamentoOrcamentoFormSet, ItemOrcamentoOrcamentoUpdateFormSet
from app.mixins import OrcamentoMixin
from app.conf import ORCAMENTO_DETAIL_URL_NAME, ORCAMENTO_LIST_URL_NAME

from django_datatables_view.base_datatable_view import BaseDatatableView

import django_filters


class OrcamentoFormSetManagement(object):
    formsets = [ItemOrcamentoOrcamentoFormSet]

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            self.object = form.save()

            for Formset in self.formsets:
                formset = context["{}set".format(str(Formset.model.__name__).lower())]
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()
        return super(OrcamentoFormSetManagement, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(OrcamentoFormSetManagement, self).get_context_data(**kwargs)
        for Formset in self.formsets:
            if self.request.POST:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(self.request.POST,
                                                                                    self.request.FILES,
                                                                                    instance=self.object)
            else:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(instance=self.object)
        return data


class OrcamentoUpdateFormSetManagement(OrcamentoFormSetManagement):
    formsets = [ItemOrcamentoOrcamentoUpdateFormSet]


class OrcamentoFilter(django_filters.FilterSet):
    class Meta:
        model = Orcamento
        fields = ["id", "vendedor__id", "cliente__nome", "forma_pagamento__tipo", "valor_total"]


class List(LoginRequiredMixin, OrcamentoMixin, ListView):
    """
    List all Orcamentos
    """
    login_url = '/admin/login/'
    template_name = 'orcamento/list.html'
    model = Orcamento
    context_object_name = 'orcamentos'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = OrcamentoFilter(self.request.GET, queryset)
        context["filter"] = filter
        return context


class ListFull(LoginRequiredMixin, OrcamentoMixin, ListView):
    """
    List all Orcamentos
    """
    login_url = '/admin/login/'
    template_name = 'orcamento/list_full.html'
    model = Orcamento
    context_object_name = 'orcamentos'
    ordering = '-id'
    paginate_by = 10
    search = ''

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = OrcamentoFilter(self.request.GET, queryset)
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
                    valor_total__icontains=search))
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
        filter = OrcamentoFilter(self.request.GET, queryset)
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


class Create(LoginRequiredMixin, OrcamentoMixin, PermissionRequiredMixin, OrcamentoFormSetManagement, CreateView):
    """
    Create a Orcamento
    """
    login_url = '/admin/login/'
    model = Orcamento
    permission_required = (
        'app.add_orcamento'
    )
    form_class = OrcamentoForm
    template_name = 'orcamento/create.html'
    context_object_name = 'orcamento'

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy(ORCAMENTO_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_initial(self):
        data = super(Create, self).get_initial()
        data['vendedor'] = self.request.user.vendedor_set.first()
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Orcamento criado com sucesso')
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Create, self).form_invalid(form)


class Detail(LoginRequiredMixin, OrcamentoMixin, DetailView):
    """
    Detail of a Orcamento
    """
    login_url = '/admin/login/'
    model = Orcamento
    template_name = 'orcamento/detail.html'
    context_object_name = 'orcamento'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        return context


class Update(LoginRequiredMixin, OrcamentoMixin, PermissionRequiredMixin, OrcamentoUpdateFormSetManagement, UpdateView):
    """
    Update a Orcamento
    """
    login_url = '/admin/login/'
    model = Orcamento
    template_name = 'orcamento/update.html'
    context_object_name = 'orcamento'
    form_class = OrcamentoForm
    permission_required = (
        'app.change_orcamento'
    )

    def get_initial(self):
        data = super(Update, self).get_initial()
        return data

    def get_success_url(self):
        return reverse_lazy(ORCAMENTO_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_context_data(self, **kwargs):
        data = super(Update, self).get_context_data(**kwargs)
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Orcamento atualizado com sucesso')
        return super(Update, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Update, self).form_invalid(form)


class Delete(LoginRequiredMixin, OrcamentoMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete a Orcamento
    """
    login_url = '/admin/login/'
    model = Orcamento
    permission_required = (
        'app.delete_orcamento'
    )
    template_name = 'orcamento/delete.html'
    context_object_name = 'orcamento'

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        collector = NestedObjects(using='default')
        collector.collect([self.get_object()])
        context['deleted_objects'] = collector.nested()
        return context

    def __init__(self):
        super(Delete, self).__init__()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Orcamento removido com sucesso')
        return super(Delete, self).delete(self.request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(ORCAMENTO_LIST_URL_NAME)


class OrcamentoListJson(BaseDatatableView):
    model = Orcamento
    columns = ("id", "vendedor", "cliente", "forma_pagamento", "valor_total", "alterado_em")
    order_columns = ["id", "vendedor__id", "cliente__nome", "forma_pagamento__tipo", "valor_total"]
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(id__icontains=search) | Q(vendedor__id__icontains=search) | Q(cliente__nome__icontains=search) | Q(
                    forma_pagamento__tipo__icontains=search) | Q(valor_total__icontains=search))
        filter = OrcamentoFilter(self.request.GET, qs)
        return filter.qs


def create_pedido_by_orcamento(request, id):
    try:
        orcamento = Orcamento.objects.get(id=id)
        pedido = Pedido()
        pedido.status = StatusPedido.objects.get(nome_status='Aberto')
        pedido.valor_total = orcamento.valor_total
        pedido.cliente = orcamento.cliente
        pedido.forma_pagamento = orcamento.forma_pagamento
        pedido.vendedor = orcamento.vendedor
        pedido.save()

        for item_orcamento in orcamento.itemorcamento_set.all():
            item_pedido = ItemPedido()
            item_pedido.pedido = pedido
            item_pedido.item = item_orcamento.item
            item_pedido.valor_total = item_orcamento.valor_total
            item_pedido.qtd = item_orcamento.qtd
            item_pedido.save()
        messages.success(request, 'Pedido criado com sucesso')
        return redirect('/')
    except (Exception,):
        messages.error(request, 'Houve algum erro, tente novamente')
        return redirect('/orcamento/')


