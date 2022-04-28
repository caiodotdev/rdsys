from django import forms
from django.forms import ModelForm, inlineformset_factory

from app.utils import generate_bootstrap_widgets_for_all_fields
from . import (
    models
)


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # field.widget.attrs['class'] = 'form-control'
            if field_name == 'phone' or field_name == 'telefone':
                field.widget.attrs['class'] = 'form-control telefone phone'
            if field_name == 'cep' or field_name == 'postalcode':
                field.widget.attrs['class'] = 'form-control cep'


class ClienteForm(BaseForm, ModelForm):
    class Meta:
        model = models.Cliente
        fields = (
            "id", "nome", "cep", "endereco", "numero", "bairro", "cidade", "estado", "telefone", "cpf", "cnpj",
            "email", "instagram", "tipo")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Cliente)

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)


class ClienteFormToInline(BaseForm, ModelForm):
    class Meta:
        model = models.Cliente
        fields = (
            "id", "nome", "cep", "endereco", "numero", "bairro", "cidade", "estado", "telefone", "cpf", "cnpj",
            "email", "instagram", "tipo")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Cliente)

    def __init__(self, *args, **kwargs):
        super(ClienteFormToInline, self).__init__(*args, **kwargs)


class VendedorForm(BaseForm, ModelForm):
    class Meta:
        model = models.Vendedor
        fields = ("id", "user")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Vendedor)

    def __init__(self, *args, **kwargs):
        super(VendedorForm, self).__init__(*args, **kwargs)


class VendedorFormToInline(BaseForm, ModelForm):
    class Meta:
        model = models.Vendedor
        fields = ("id", "user")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Vendedor)

    def __init__(self, *args, **kwargs):
        super(VendedorFormToInline, self).__init__(*args, **kwargs)


VendedorUserFormSet = inlineformset_factory(models.User, models.Vendedor, form=VendedorFormToInline, extra=1)


class FormaPagamentoForm(BaseForm, ModelForm):
    class Meta:
        model = models.FormaPagamento
        fields = ("id", "tipo")
        widgets = generate_bootstrap_widgets_for_all_fields(models.FormaPagamento)

    def __init__(self, *args, **kwargs):
        super(FormaPagamentoForm, self).__init__(*args, **kwargs)


class FormaPagamentoFormToInline(BaseForm, ModelForm):
    class Meta:
        model = models.FormaPagamento
        fields = ("id", "tipo")
        widgets = generate_bootstrap_widgets_for_all_fields(models.FormaPagamento)

    def __init__(self, *args, **kwargs):
        super(FormaPagamentoFormToInline, self).__init__(*args, **kwargs)


class StatusPedidoForm(BaseForm, ModelForm):
    class Meta:
        model = models.StatusPedido
        fields = ("id", "nome_status")
        widgets = generate_bootstrap_widgets_for_all_fields(models.StatusPedido)

    def __init__(self, *args, **kwargs):
        super(StatusPedidoForm, self).__init__(*args, **kwargs)


class StatusPedidoFormToInline(BaseForm, ModelForm):
    class Meta:
        model = models.StatusPedido
        fields = ("id", "nome_status", "cor")
        widgets = generate_bootstrap_widgets_for_all_fields(models.StatusPedido)

    def __init__(self, *args, **kwargs):
        super(StatusPedidoFormToInline, self).__init__(*args, **kwargs)


class PedidoForm(BaseForm, ModelForm):
    class Meta:
        model = models.Pedido
        fields = ("id", "vendedor", "cliente", "forma_pagamento", "status", "descricao", "valor_total")

    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)


class PedidoFormToInline(BaseForm, ModelForm):
    class Meta:
        model = models.Pedido
        fields = ("id", "vendedor", "cliente", "forma_pagamento", "status", "valor_total")

    def __init__(self, *args, **kwargs):
        super(PedidoFormToInline, self).__init__(*args, **kwargs)


PedidoVendedorFormSet = inlineformset_factory(models.Vendedor, models.Pedido, form=PedidoFormToInline, extra=1)

PedidoClienteFormSet = inlineformset_factory(models.Cliente, models.Pedido, form=PedidoFormToInline, extra=1)

PedidoClienteUpdateFormSet = inlineformset_factory(models.Cliente, models.Pedido, form=PedidoFormToInline, extra=0)

PedidoFormaPagamentoFormSet = inlineformset_factory(models.FormaPagamento, models.Pedido, form=PedidoFormToInline,
                                                    extra=1)

PedidoStatusPedidoFormSet = inlineformset_factory(models.StatusPedido, models.Pedido, form=PedidoFormToInline, extra=1)


class ItemForm(BaseForm, ModelForm):
    class Meta:
        model = models.Item
        fields = ("id", "descricao", "preco_custo", "valor_unitario", "foto")

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)


class ItemFormToInline(BaseForm, ModelForm):
    class Meta:
        model = models.Item
        fields = ("id", "descricao", "preco_custo", "valor_unitario", "foto")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Item)

    def __init__(self, *args, **kwargs):
        super(ItemFormToInline, self).__init__(*args, **kwargs)


class ItemPedidoForm(BaseForm, ModelForm):
    class Meta:
        model = models.ItemPedido
        fields = ("id", "pedido", "qtd", "item", "valor_total")

    def __init__(self, *args, **kwargs):
        super(ItemPedidoForm, self).__init__(*args, **kwargs)


class ItemPedidoFormToInline(BaseForm, ModelForm):
    class Meta:
        model = models.ItemPedido
        fields = ("id", "pedido", "qtd", "item", "valor_total")

    def __init__(self, *args, **kwargs):
        super(ItemPedidoFormToInline, self).__init__(*args, **kwargs)


ItemPedidoPedidoFormSet = inlineformset_factory(models.Pedido, models.ItemPedido, form=ItemPedidoFormToInline, extra=1)

ItemPedidoPedidoUpdateFormSet = inlineformset_factory(models.Pedido, models.ItemPedido, form=ItemPedidoFormToInline,
                                                      extra=0)

ItemPedidoItemFormSet = inlineformset_factory(models.Item, models.ItemPedido, form=ItemPedidoFormToInline, extra=1)


class OrcamentoForm(BaseForm, ModelForm):
    class Meta:
        model = models.Orcamento
        fields = ("id", "vendedor", "cliente", "forma_pagamento", "valor_total")

    def __init__(self, *args, **kwargs):
        super(OrcamentoForm, self).__init__(*args, **kwargs)


class OrcamentoFormToInline(BaseForm, ModelForm):
    class Meta:
        model = models.Orcamento
        fields = ("id", "vendedor", "cliente", "forma_pagamento", "valor_total")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Orcamento)

    def __init__(self, *args, **kwargs):
        super(OrcamentoFormToInline, self).__init__(*args, **kwargs)


OrcamentoVendedorFormSet = inlineformset_factory(models.Vendedor, models.Orcamento, form=OrcamentoFormToInline, extra=1)

OrcamentoClienteFormSet = inlineformset_factory(models.Cliente, models.Orcamento, form=OrcamentoFormToInline, extra=1)

OrcamentoFormaPagamentoFormSet = inlineformset_factory(models.FormaPagamento, models.Orcamento,
                                                       form=OrcamentoFormToInline, extra=1)


class ItemOrcamentoForm(BaseForm, ModelForm):
    class Meta:
        model = models.ItemOrcamento
        fields = ("id", "orcamento", "qtd", "item", "valor_total")
        widgets = generate_bootstrap_widgets_for_all_fields(models.ItemOrcamento)

    def __init__(self, *args, **kwargs):
        super(ItemOrcamentoForm, self).__init__(*args, **kwargs)


class ItemOrcamentoFormToInline(BaseForm, ModelForm):
    class Meta:
        model = models.ItemOrcamento
        fields = ("id", "orcamento", "qtd", "item", "valor_total")

    def __init__(self, *args, **kwargs):
        super(ItemOrcamentoFormToInline, self).__init__(*args, **kwargs)


ItemOrcamentoOrcamentoFormSet = inlineformset_factory(models.Orcamento, models.ItemOrcamento,
                                                      form=ItemOrcamentoFormToInline, extra=1)

ItemOrcamentoOrcamentoUpdateFormSet = inlineformset_factory(models.Orcamento, models.ItemOrcamento,
                                                      form=ItemOrcamentoFormToInline, extra=0)

ItemOrcamentoItemFormSet = inlineformset_factory(models.Item, models.ItemOrcamento, form=ItemOrcamentoFormToInline,
                                                 extra=1)
