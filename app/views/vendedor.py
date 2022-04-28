#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import FieldDoesNotExist
from django.db import transaction
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, DeleteView, UpdateView
)
from django.views.generic.list import ListView

from django.db.models import Q


try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy, reverse

from app.models import Vendedor
from app.forms import VendedorForm, PedidoVendedorFormSet
from app.mixins import VendedorMixin
from app.conf import VENDEDOR_DETAIL_URL_NAME, VENDEDOR_LIST_URL_NAME

from django_datatables_view.base_datatable_view import BaseDatatableView

from app.utils import upload_image, upload_file

import django_filters

class VendedorFormSetManagement(object):
    formsets = [PedidoVendedorFormSet]

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            self.object = form.save()
            
            for Formset in self.formsets:
                formset = context["{}set".format(str(Formset.model.__name__).lower())]
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()
        return super(VendedorFormSetManagement, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(VendedorFormSetManagement, self).get_context_data(**kwargs)
        for Formset in self.formsets:
            if self.request.POST:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(self.request.POST,
                                                                                    self.request.FILES,
                                                                                    instance=self.object)
            else:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(instance=self.object)
        return data


class VendedorFilter(django_filters.FilterSet):
    class Meta:
        model = Vendedor
        fields = ["id", "user__id"]


class List(LoginRequiredMixin, VendedorMixin, ListView):
    """
    List all Vendedors
    """
    login_url = '/admin/login/'
    template_name = 'vendedor/list.html'
    model = Vendedor
    context_object_name = 'vendedors'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = VendedorFilter(self.request.GET, queryset)
        context["filter"] = filter
        return context


class ListFull(LoginRequiredMixin, VendedorMixin, ListView):
    """
    List all Vendedors
    """
    login_url = '/admin/login/'
    template_name = 'vendedor/list_full.html'
    model = Vendedor
    context_object_name = 'vendedors'
    ordering = '-id'
    paginate_by = 10
    search = ''

    def get_queryset(self):
        queryset = super().get_queryset()
        filter =  VendedorFilter(self.request.GET, queryset)
        queryset = self.search_general(filter.qs)
        queryset = self.ordering_data(queryset)
        return queryset

    def search_general(self, qs):
        if 'search' in self.request.GET:
            self.search = self.request.GET['search']
            if self.search:
                search = self.search
                qs = qs.filter(Q(id__icontains=search)| Q(user__id__icontains=search))
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
        filter = VendedorFilter(self.request.GET, queryset)
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


class Create(LoginRequiredMixin, VendedorMixin, PermissionRequiredMixin, VendedorFormSetManagement, CreateView):
    """
    Create a Vendedor
    """
    login_url = '/admin/login/'
    model = Vendedor
    permission_required = (
        'app.add_vendedor'
    )
    form_class = VendedorForm
    template_name = 'vendedor/create.html'
    context_object_name = 'vendedor'

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy(VENDEDOR_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_initial(self):
        data = super(Create, self).get_initial()
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Vendedor criado com sucesso')
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Create, self).form_invalid(form)


class Detail(LoginRequiredMixin, VendedorMixin, DetailView):
    """
    Detail of a Vendedor
    """
    login_url = '/admin/login/'
    model = Vendedor
    template_name = 'vendedor/detail.html'
    context_object_name = 'vendedor'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        return context


class Update(LoginRequiredMixin, VendedorMixin, PermissionRequiredMixin, VendedorFormSetManagement, UpdateView):
    """
    Update a Vendedor
    """
    login_url = '/admin/login/'
    model = Vendedor
    template_name = 'vendedor/update.html'
    context_object_name = 'vendedor'
    form_class = VendedorForm
    permission_required = (
        'app.change_vendedor'
    )

    def get_initial(self):
        data = super(Update, self).get_initial()
        return data

    def get_success_url(self):
        return reverse_lazy(VENDEDOR_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_context_data(self, **kwargs):
        data = super(Update, self).get_context_data(**kwargs)
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Vendedor atualizado com sucesso')
        return super(Update, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Update, self).form_invalid(form)


class Delete(LoginRequiredMixin, VendedorMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete a Vendedor
    """
    login_url = '/admin/login/'
    model = Vendedor
    permission_required = (
        'app.delete_vendedor'
    )
    template_name = 'vendedor/delete.html'
    context_object_name = 'vendedor'

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        collector = NestedObjects(using='default')
        collector.collect([self.get_object()])
        context['deleted_objects'] = collector.nested()
        return context

    def __init__(self):
        super(Delete, self).__init__()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Vendedor removido com sucesso')
        return super(Delete, self).delete(self.request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(VENDEDOR_LIST_URL_NAME)


class VendedorListJson(BaseDatatableView):
    model = Vendedor
    columns = ("id", "user")
    order_columns = ["id", "user__id"]
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(id__icontains=search)| Q(user__id__icontains=search))
        filter = VendedorFilter(self.request.GET, qs)
        return filter.qs
