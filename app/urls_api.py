from rest_framework.routers import DefaultRouter

from app import (
    viewsets
)

api_urlpatterns = []

cliente_router = DefaultRouter()

cliente_router.register(
    r'^api/cliente',
    viewsets.ClienteViewSet,
    basename="cliente"
)

api_urlpatterns += cliente_router.urls
vendedor_router = DefaultRouter()

vendedor_router.register(
    r'^api/vendedor',
    viewsets.VendedorViewSet,
    basename="vendedor"
)

api_urlpatterns += vendedor_router.urls
formapagamento_router = DefaultRouter()

formapagamento_router.register(
    r'^api/formapagamento',
    viewsets.FormaPagamentoViewSet,
    basename="formapagamento"
)

api_urlpatterns += formapagamento_router.urls
statuspedido_router = DefaultRouter()

statuspedido_router.register(
    r'^api/statuspedido',
    viewsets.StatusPedidoViewSet,
    basename="statuspedido"
)

api_urlpatterns += statuspedido_router.urls
pedido_router = DefaultRouter()

pedido_router.register(
    r'^api/pedido',
    viewsets.PedidoViewSet,
    basename="pedido"
)

api_urlpatterns += pedido_router.urls
item_router = DefaultRouter()

item_router.register(
    r'^api/item',
    viewsets.ItemViewSet,
    basename="item"
)

api_urlpatterns += item_router.urls
itempedido_router = DefaultRouter()

itempedido_router.register(
    r'^api/itempedido',
    viewsets.ItemPedidoViewSet,
    basename="itempedido"
)

api_urlpatterns += itempedido_router.urls
orcamento_router = DefaultRouter()

orcamento_router.register(
    r'^api/orcamento',
    viewsets.OrcamentoViewSet,
    basename="orcamento"
)

api_urlpatterns += orcamento_router.urls
itemorcamento_router = DefaultRouter()

itemorcamento_router.register(
    r'^api/itemorcamento',
    viewsets.ItemOrcamentoViewSet,
    basename="itemorcamento"
)

api_urlpatterns += itemorcamento_router.urls
