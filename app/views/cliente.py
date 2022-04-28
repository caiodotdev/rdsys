#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from app.models import Cliente, Pedido
from app.forms import ClienteForm, PedidoClienteFormSet, PedidoClienteUpdateFormSet
from app.mixins import ClienteMixin
from app.conf import CLIENTE_DETAIL_URL_NAME, CLIENTE_LIST_URL_NAME

from django_datatables_view.base_datatable_view import BaseDatatableView

import django_filters


class ClienteFormSetManagement(object):
    formsets = [PedidoClienteFormSet]

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            self.object = form.save()

            for Formset in self.formsets:
                formset = context["{}set".format(str(Formset.model.__name__).lower())]
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()
        return super(ClienteFormSetManagement, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(ClienteFormSetManagement, self).get_context_data(**kwargs)
        for Formset in self.formsets:
            if self.request.POST:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(self.request.POST,
                                                                                    self.request.FILES,
                                                                                    instance=self.object)
            else:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(instance=self.object)
        return data


class ClienteUpdateFormSetManagement(ClienteFormSetManagement):
    formsets = [PedidoClienteUpdateFormSet]


class ClienteFilter(django_filters.FilterSet):
    class Meta:
        model = Cliente
        fields = ["id", "nome", "cep", "endereco", "latitude", "longitude", "numero", "cidade", "telefone", "cpf",
                  "cnpj", "email", "instagram", "tipo"]


class List(LoginRequiredMixin, ClienteMixin, ListView):
    """
    List all Clientes
    """
    login_url = '/admin/login/'
    template_name = 'cliente/list.html'
    model = Cliente
    context_object_name = 'clientes'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = ClienteFilter(self.request.GET, queryset)
        context["filter"] = filter
        context['clientes_novos'] = Cliente.objects.filter(tipo='Novo').count()
        context['clientes_padrao'] = Cliente.objects.filter(tipo='Normal').count()
        context['total_clientes'] = Cliente.objects.all().count()
        return context


class ListFull(LoginRequiredMixin, ClienteMixin, ListView):
    """
    List all Clientes
    """
    login_url = '/admin/login/'
    template_name = 'cliente/list_full.html'
    model = Cliente
    context_object_name = 'clientes'
    ordering = '-id'
    paginate_by = 10
    search = ''

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = ClienteFilter(self.request.GET, queryset)
        queryset = self.search_general(filter.qs)
        queryset = self.ordering_data(queryset)
        return queryset

    def search_general(self, qs):
        if 'search' in self.request.GET:
            self.search = self.request.GET['search']
            if self.search:
                search = self.search
                qs = qs.filter(Q(id__icontains=search) | Q(nome__icontains=search) | Q(cep__icontains=search) | Q(
                    endereco__icontains=search) | Q(latitude__icontains=search) | Q(longitude__icontains=search) | Q(
                    numero__icontains=search) | Q(cidade__icontains=search) | Q(telefone__icontains=search) | Q(
                    cpf__icontains=search) | Q(cnpj__icontains=search) | Q(email__icontains=search) | Q(
                    instagram__icontains=search) | Q(tipo__icontains=search))
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
        filter = ClienteFilter(self.request.GET, queryset)
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


class Create(LoginRequiredMixin, ClienteMixin, PermissionRequiredMixin, CreateView):
    """
    Create a Cliente
    """
    login_url = '/admin/login/'
    model = Cliente
    permission_required = (
        'app.add_cliente'
    )
    form_class = ClienteForm
    template_name = 'cliente/create.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy(CLIENTE_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_initial(self):
        data = super(Create, self).get_initial()
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Cliente criado com sucesso')
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Create, self).form_invalid(form)


class Detail(LoginRequiredMixin, ClienteMixin, DetailView):
    """
    Detail of a Cliente
    """
    login_url = '/admin/login/'
    model = Cliente
    template_name = 'cliente/detail.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        return context


class Update(LoginRequiredMixin, ClienteMixin, PermissionRequiredMixin, ClienteUpdateFormSetManagement, UpdateView):
    """
    Update a Cliente
    """
    login_url = '/admin/login/'
    model = Cliente
    template_name = 'cliente/update.html'
    context_object_name = 'cliente'
    form_class = ClienteForm
    permission_required = (
        'app.change_cliente'
    )

    def get_initial(self):
        data = super(Update, self).get_initial()
        return data

    def get_success_url(self):
        return reverse_lazy(CLIENTE_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_context_data(self, **kwargs):
        data = super(Update, self).get_context_data(**kwargs)
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Cliente atualizado com sucesso')
        return super(Update, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Update, self).form_invalid(form)


class Delete(LoginRequiredMixin, ClienteMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete a Cliente
    """
    login_url = '/admin/login/'
    model = Cliente
    permission_required = (
        'app.delete_cliente'
    )
    template_name = 'cliente/delete.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        collector = NestedObjects(using='default')
        collector.collect([self.get_object()])
        context['deleted_objects'] = collector.nested()
        return context

    def __init__(self):
        super(Delete, self).__init__()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cliente removido com sucesso')
        return super(Delete, self).delete(self.request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(CLIENTE_LIST_URL_NAME)


class ClienteListJson(BaseDatatableView):
    model = Cliente
    columns = (
        "id", "nome", "endereco", "numero", "telefone", "email",
        "tipo", "alterado_em")
    order_columns = ["id", "nome", "endereco", "numero", "telefone", "email",
                     "tipo"]
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(id__icontains=search) | Q(nome__icontains=search) | Q(cep__icontains=search) | Q(
                endereco__icontains=search) | Q(
                numero__icontains=search) | Q(cidade__icontains=search) | Q(telefone__icontains=search) | Q(
                cpf__icontains=search) | Q(cnpj__icontains=search) | Q(email__icontains=search) | Q(
                instagram__icontains=search) | Q(tipo__icontains=search))
        filter = ClienteFilter(self.request.GET, qs)
        return filter.qs


class PedidosDoClienteListJson(BaseDatatableView):
    model = Pedido
    columns = ("id", "forma_pagamento", "valor_total", "vendedor", "criado_em", "status", "alterado_em")
    order_columns = ["id", "forma_pagamento", "valor_total", "vendedor", "criado_em", "status"]
    max_display_length = 500

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'criado_em':
            # escape HTML for security reasons
            return row.criado_em.strftime("%d-%m-%Y %H:%M:%S")
        else:
            return super(PedidosDoClienteListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(id__icontains=search) | Q(vendedor__id__icontains=search) | Q(cliente__nome__icontains=search) | Q(
                    forma_pagamento__tipo__icontains=search) | Q(status__nome_status__icontains=search) | Q(
                    valor_total__icontains=search))
        return qs

    def get_initial_queryset(self):
        return self.model.objects.filter(cliente_id=self.kwargs['id'])
