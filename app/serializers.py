from rest_framework import serializers

from app.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = (
        "id", "nome", "cep", "endereco", "latitude", "longitude", "numero", "cidade", "telefone", "cpf", "cnpj",
        "email", "instagram", "tipo")


from app.models import Vendedor


class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ("id", "user")


from app.models import FormaPagamento


class FormaPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPagamento
        fields = ("id", "tipo")


from app.models import StatusPedido


class StatusPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusPedido
        fields = ("id", "nome_status")


from app.models import Pedido


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ("id", "vendedor", "cliente", "forma_pagamento", "status", "valor_total")


from app.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "descricao", "preco_custo", "valor_unitario", "foto")


from app.models import ItemPedido


class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ("id", "pedido", "qtd", "item", "valor_total")
from app.models import Orcamento
class OrcamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orcamento
        fields = ("id", "vendedor", "cliente", "forma_pagamento", "valor_total")


from app.models import ItemOrcamento
class ItemOrcamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrcamento
        fields = ("id", "orcamento", "qtd", "item", "valor_total")


