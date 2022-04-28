import django_filters
from django_filters import rest_framework as filters
from rest_framework import viewsets

from . import (
    serializers,
    models
)


class ClienteFilter(django_filters.FilterSet):
    class Meta:
        model = models.Cliente
        fields = ["id", "nome", "cep", "endereco", "latitude", "longitude", "numero", "cidade", "telefone", "cpf",
                  "cnpj", "email", "instagram", "tipo"]


class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClienteSerializer
    queryset = models.Cliente.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ClienteFilter


class VendedorFilter(django_filters.FilterSet):
    class Meta:
        model = models.Vendedor
        fields = ["id", "user__id"]


class VendedorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VendedorSerializer
    queryset = models.Vendedor.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VendedorFilter


class FormaPagamentoFilter(django_filters.FilterSet):
    class Meta:
        model = models.FormaPagamento
        fields = ["id", "tipo"]


class FormaPagamentoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FormaPagamentoSerializer
    queryset = models.FormaPagamento.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FormaPagamentoFilter


class StatusPedidoFilter(django_filters.FilterSet):
    class Meta:
        model = models.StatusPedido
        fields = ["id", "nome_status"]


class StatusPedidoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StatusPedidoSerializer
    queryset = models.StatusPedido.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StatusPedidoFilter


class PedidoFilter(django_filters.FilterSet):
    class Meta:
        model = models.Pedido
        fields = ["id", "vendedor__id", "cliente__nome", "forma_pagamento__tipo", "status__nome_status", "valor_total"]


class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PedidoSerializer
    queryset = models.Pedido.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PedidoFilter


class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = models.Item
        fields = ["id", "descricao", "preco_custo", "valor_unitario", "foto"]


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ItemSerializer
    queryset = models.Item.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ItemFilter


class ItemPedidoFilter(django_filters.FilterSet):
    class Meta:
        model = models.ItemPedido
        fields = ["id", "pedido__id", "qtd", "item__descricao", "valor_total"]


class ItemPedidoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ItemPedidoSerializer
    queryset = models.ItemPedido.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ItemPedidoFilter


class OrcamentoFilter(django_filters.FilterSet):
    class Meta:
        model = models.Orcamento
        fields = ["id", "vendedor__id", "cliente__nome", "forma_pagamento__tipo", "valor_total"]


class OrcamentoViewSet(viewsets.ModelViewSet):
    
    serializer_class = serializers.OrcamentoSerializer
    queryset = models.Orcamento.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrcamentoFilter



class ItemOrcamentoFilter(django_filters.FilterSet):
    class Meta:
        model = models.ItemOrcamento
        fields = ["id", "orcamento__id", "qtd", "item__descricao", "valor_total"]


class ItemOrcamentoViewSet(viewsets.ModelViewSet):
    
    serializer_class = serializers.ItemOrcamentoSerializer
    queryset = models.ItemOrcamento.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ItemOrcamentoFilter

