import datetime

from django import template
from django.db.models import Sum
from django.template.loader import get_template

register = template.Library()


@register.filter()
def num_pedidos(cliente):
    today = datetime.datetime.now()
    return cliente.pedido_set.filter(criado_em__year=today.year).count()


@register.filter()
def receita_gerada(cliente):
    today = datetime.datetime.now()
    qs = cliente.pedido_set.filter(criado_em__year=today.year)
    if qs:
        return "{:.2f}".format(qs.aggregate(Sum('valor_total'))['valor_total__sum'])
    else:
        return "0.00"


@register.filter()
def get_fields(obj):
    return [(field.name, field.value_to_string(obj)) for field in obj._meta.fields]


@register.filter("add_formset_element")
def add_formset_element_js(formset):
    # We just use the first column
    if len(formset) > 0:
        row = formset[0]
        for input in row:
            tokens = input.html_name.split("-")
            new_text = ""
            for token in tokens:
                new_token_text = ""
                try:
                    int(token)
                    new_token_text = "{{id}}"
                except ValueError:
                    new_token_text = token
                new_text += new_token_text + "-"
            new_text = new_text[:-1]
            input.html_name = new_text
        return get_template("base/add_formset_underscore.html").render({"form": row})
    return ""


@register.simple_tag(name="formset_js")
def formset_js():
    return get_template("base/add_formset_underscore_js.html").render()
