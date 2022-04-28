from django.core.exceptions import FieldDoesNotExist

from app.models import (
    Cliente, Vendedor, FormaPagamento, StatusPedido, Pedido, Item, ItemPedido
)


class ClienteMixin(object):

    def kwargs_for_reverse_url(self):
        kwargs_dict = dict()
        if self.model:
            self.object = self.object if self.object is not None else self.get_object()
            try:
                self.model._meta.get_field('slug')
                kwargs_dict['slug'] = self.object.slug
            except FieldDoesNotExist:
                kwargs_dict['pk'] = self.object.id
        return kwargs_dict

    def get_context_data(self, **kwargs):
        context = super(ClienteMixin, self).get_context_data(**kwargs)
        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        return context

    def get_cliente(self):
        return Cliente.objects.get(pk=self.kwargs.get("pk_cliente", 0))


class VendedorMixin(object):

    def kwargs_for_reverse_url(self):
        kwargs_dict = dict()
        if self.model:
            self.object = self.object if self.object is not None else self.get_object()
            try:
                self.model._meta.get_field('slug')
                kwargs_dict['slug'] = self.object.slug
            except FieldDoesNotExist:
                kwargs_dict['pk'] = self.object.id
        return kwargs_dict

    def get_context_data(self, **kwargs):
        context = super(VendedorMixin, self).get_context_data(**kwargs)
        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        return context

    def get_vendedor(self):
        return Vendedor.objects.get(pk=self.kwargs.get("pk_vendedor", 0))


class FormaPagamentoMixin(object):

    def kwargs_for_reverse_url(self):
        kwargs_dict = dict()
        if self.model:
            self.object = self.object if self.object is not None else self.get_object()
            try:
                self.model._meta.get_field('slug')
                kwargs_dict['slug'] = self.object.slug
            except FieldDoesNotExist:
                kwargs_dict['pk'] = self.object.id
        return kwargs_dict

    def get_context_data(self, **kwargs):
        context = super(FormaPagamentoMixin, self).get_context_data(**kwargs)
        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        return context

    def get_formapagamento(self):
        return FormaPagamento.objects.get(pk=self.kwargs.get("pk_formapagamento", 0))


class StatusPedidoMixin(object):

    def kwargs_for_reverse_url(self):
        kwargs_dict = dict()
        if self.model:
            self.object = self.object if self.object is not None else self.get_object()
            try:
                self.model._meta.get_field('slug')
                kwargs_dict['slug'] = self.object.slug
            except FieldDoesNotExist:
                kwargs_dict['pk'] = self.object.id
        return kwargs_dict

    def get_context_data(self, **kwargs):
        context = super(StatusPedidoMixin, self).get_context_data(**kwargs)
        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        return context

    def get_statuspedido(self):
        return StatusPedido.objects.get(pk=self.kwargs.get("pk_statuspedido", 0))


class PedidoMixin(object):

    def kwargs_for_reverse_url(self):
        kwargs_dict = dict()
        if self.model:
            self.object = self.object if self.object is not None else self.get_object()
            try:
                self.model._meta.get_field('slug')
                kwargs_dict['slug'] = self.object.slug
            except FieldDoesNotExist:
                kwargs_dict['pk'] = self.object.id
        return kwargs_dict

    def get_context_data(self, **kwargs):
        context = super(PedidoMixin, self).get_context_data(**kwargs)
        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        return context

    def get_pedido(self):
        return Pedido.objects.get(pk=self.kwargs.get("pk_pedido", 0))


class ItemMixin(object):

    def kwargs_for_reverse_url(self):
        kwargs_dict = dict()
        if self.model:
            self.object = self.object if self.object is not None else self.get_object()
            try:
                self.model._meta.get_field('slug')
                kwargs_dict['slug'] = self.object.slug
            except FieldDoesNotExist:
                kwargs_dict['pk'] = self.object.id
        return kwargs_dict

    def get_context_data(self, **kwargs):
        context = super(ItemMixin, self).get_context_data(**kwargs)
        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        return context

    def get_item(self):
        return Item.objects.get(pk=self.kwargs.get("pk_item", 0))


class ItemPedidoMixin(object):

    def kwargs_for_reverse_url(self):
        kwargs_dict = dict()
        if self.model:
            self.object = self.object if self.object is not None else self.get_object()
            try:
                self.model._meta.get_field('slug')
                kwargs_dict['slug'] = self.object.slug
            except FieldDoesNotExist:
                kwargs_dict['pk'] = self.object.id
        return kwargs_dict

    def get_context_data(self, **kwargs):
        context = super(ItemPedidoMixin, self).get_context_data(**kwargs)
        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        return context

    def get_itempedido(self):
        return ItemPedido.objects.get(pk=self.kwargs.get("pk_itempedido", 0))
class OrcamentoMixin(object):

    def kwargs_for_reverse_url(self):
        kwargs_dict = dict()
        if self.model:
            self.object = self.object if self.object is not None else self.get_object()
            try:
                self.model._meta.get_field('slug')
                kwargs_dict['slug'] = self.object.slug
            except FieldDoesNotExist:
                kwargs_dict['pk'] = self.object.id
        return kwargs_dict

    def get_context_data(self, **kwargs):
        context = super(OrcamentoMixin, self).get_context_data(**kwargs)
        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        return context

    def get_orcamento(self):
        return Orcamento.objects.get(pk=self.kwargs.get("pk_orcamento", 0))

class ItemOrcamentoMixin(object):

    def kwargs_for_reverse_url(self):
        kwargs_dict = dict()
        if self.model:
            self.object = self.object if self.object is not None else self.get_object()
            try:
                self.model._meta.get_field('slug')
                kwargs_dict['slug'] = self.object.slug
            except FieldDoesNotExist:
                kwargs_dict['pk'] = self.object.id
        return kwargs_dict

    def get_context_data(self, **kwargs):
        context = super(ItemOrcamentoMixin, self).get_context_data(**kwargs)
        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        return context

    def get_itemorcamento(self):
        return ItemOrcamento.objects.get(pk=self.kwargs.get("pk_itemorcamento", 0))

