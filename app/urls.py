from django.urls import path, include

from app import conf
from app.urls_api import api_urlpatterns

urlpatterns = []

urlpatterns += [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls'))
]

from app.views import cliente

urlpatterns += [
    # cliente
    path(
        'cliente/',
        cliente.List.as_view(),
        name=conf.CLIENTE_LIST_URL_NAME
    ),
    path(
        'cliente/full/',
        cliente.ListFull.as_view(),
        name='CLIENTE_list_full'
    ),
    path(
        'cliente/create/',
        cliente.Create.as_view(),
        name=conf.CLIENTE_CREATE_URL_NAME
    ),
    path(
        'cliente/<int:pk>/',
        cliente.Detail.as_view(),
        name=conf.CLIENTE_DETAIL_URL_NAME
    ),
    path(
        'cliente/<int:pk>/update/',
        cliente.Update.as_view(),
        name=conf.CLIENTE_UPDATE_URL_NAME
    ),
    path(
        'cliente/<int:pk>/delete/',
        cliente.Delete.as_view(),
        name=conf.CLIENTE_DELETE_URL_NAME
    ),
    path(
        'cliente/list/json/',
        cliente.ClienteListJson.as_view(),
        name=conf.CLIENTE_LIST_JSON_URL_NAME
    ),
    path(
        'cliente/pedidos/json/<int:id>/',
        cliente.PedidosDoClienteListJson.as_view(),
        name='pedidos_cliente_json'
    )
]

from app.views import vendedor

urlpatterns += [
    # vendedor
    path(
        'vendedor/',
        vendedor.List.as_view(),
        name=conf.VENDEDOR_LIST_URL_NAME
    ),
    path(
        'vendedor/full/',
        vendedor.ListFull.as_view(),
        name='VENDEDOR_list_full'
    ),
    path(
        'vendedor/create/',
        vendedor.Create.as_view(),
        name=conf.VENDEDOR_CREATE_URL_NAME
    ),
    path(
        'vendedor/<int:pk>/',
        vendedor.Detail.as_view(),
        name=conf.VENDEDOR_DETAIL_URL_NAME
    ),
    path(
        'vendedor/<int:pk>/update/',
        vendedor.Update.as_view(),
        name=conf.VENDEDOR_UPDATE_URL_NAME
    ),
    path(
        'vendedor/<int:pk>/delete/',
        vendedor.Delete.as_view(),
        name=conf.VENDEDOR_DELETE_URL_NAME
    ),
    path(
        'vendedor/list/json/',
        vendedor.VendedorListJson.as_view(),
        name=conf.VENDEDOR_LIST_JSON_URL_NAME
    )
]

from app.views import forma_pagamento

urlpatterns += [
    # forma_pagamento
    path(
        'formapagamento/',
        forma_pagamento.List.as_view(),
        name=conf.FORMAPAGAMENTO_LIST_URL_NAME
    ),
    path(
        'formapagamento/full/',
        forma_pagamento.ListFull.as_view(),
        name='FORMAPAGAMENTO_list_full'
    ),
    path(
        'formapagamento/create/',
        forma_pagamento.Create.as_view(),
        name=conf.FORMAPAGAMENTO_CREATE_URL_NAME
    ),
    path(
        'formapagamento/<int:pk>/',
        forma_pagamento.Detail.as_view(),
        name=conf.FORMAPAGAMENTO_DETAIL_URL_NAME
    ),
    path(
        'formapagamento/<int:pk>/update/',
        forma_pagamento.Update.as_view(),
        name=conf.FORMAPAGAMENTO_UPDATE_URL_NAME
    ),
    path(
        'formapagamento/<int:pk>/delete/',
        forma_pagamento.Delete.as_view(),
        name=conf.FORMAPAGAMENTO_DELETE_URL_NAME
    ),
    path(
        'formapagamento/list/json/',
        forma_pagamento.FormaPagamentoListJson.as_view(),
        name=conf.FORMAPAGAMENTO_LIST_JSON_URL_NAME
    )
]

from app.views import status_pedido

urlpatterns += [
    # status_pedido
    path(
        'statuspedido/',
        status_pedido.List.as_view(),
        name=conf.STATUSPEDIDO_LIST_URL_NAME
    ),
    path(
        'statuspedido/full/',
        status_pedido.ListFull.as_view(),
        name='STATUSPEDIDO_list_full'
    ),
    path(
        'statuspedido/create/',
        status_pedido.Create.as_view(),
        name=conf.STATUSPEDIDO_CREATE_URL_NAME
    ),
    path(
        'statuspedido/<int:pk>/',
        status_pedido.Detail.as_view(),
        name=conf.STATUSPEDIDO_DETAIL_URL_NAME
    ),
    path(
        'statuspedido/<int:pk>/update/',
        status_pedido.Update.as_view(),
        name=conf.STATUSPEDIDO_UPDATE_URL_NAME
    ),
    path(
        'statuspedido/<int:pk>/delete/',
        status_pedido.Delete.as_view(),
        name=conf.STATUSPEDIDO_DELETE_URL_NAME
    ),
    path(
        'statuspedido/list/json/',
        status_pedido.StatusPedidoListJson.as_view(),
        name=conf.STATUSPEDIDO_LIST_JSON_URL_NAME
    )
]

from app.views import pedido

urlpatterns += [
    # pedido
    path(
        '',
        pedido.List.as_view(),
        name=conf.PEDIDO_LIST_URL_NAME
    ),
    path(
        'pedido/full/',
        pedido.ListFull.as_view(),
        name='PEDIDO_list_full'
    ),
    path(
        'pedido/create/',
        pedido.Create.as_view(),
        name=conf.PEDIDO_CREATE_URL_NAME
    ),
    path(
        'pedido/<int:pk>/',
        pedido.Detail.as_view(),
        name=conf.PEDIDO_DETAIL_URL_NAME
    ),
    path(
        'pedido/<int:pk>/update/',
        pedido.Update.as_view(),
        name=conf.PEDIDO_UPDATE_URL_NAME
    ),
    path(
        'pedido/<int:pk>/delete/',
        pedido.Delete.as_view(),
        name=conf.PEDIDO_DELETE_URL_NAME
    ),
    path(
        'pedido/list/json/',
        pedido.PedidoListJson.as_view(),
        name=conf.PEDIDO_LIST_JSON_URL_NAME
    )
]

from app.views import item

urlpatterns += [
    # item
    path(
        'item/',
        item.List.as_view(),
        name=conf.ITEM_LIST_URL_NAME
    ),
    path(
        'item/full/',
        item.ListFull.as_view(),
        name='ITEM_list_full'
    ),
    path(
        'item/create/',
        item.Create.as_view(),
        name=conf.ITEM_CREATE_URL_NAME
    ),
    path(
        'item/<int:pk>/',
        item.Detail.as_view(),
        name=conf.ITEM_DETAIL_URL_NAME
    ),
    path(
        'item/<int:pk>/update/',
        item.Update.as_view(),
        name=conf.ITEM_UPDATE_URL_NAME
    ),
    path(
        'item/<int:pk>/delete/',
        item.Delete.as_view(),
        name=conf.ITEM_DELETE_URL_NAME
    ),
    path(
        'item/list/json/',
        item.ItemListJson.as_view(),
        name=conf.ITEM_LIST_JSON_URL_NAME
    )
]

from app.views import item_pedido

urlpatterns += [
    # item_pedido
    path(
        'itempedido/',
        item_pedido.List.as_view(),
        name=conf.ITEMPEDIDO_LIST_URL_NAME
    ),
    path(
        'itempedido/full/',
        item_pedido.ListFull.as_view(),
        name='ITEMPEDIDO_list_full'
    ),
    path(
        'itempedido/create/',
        item_pedido.Create.as_view(),
        name=conf.ITEMPEDIDO_CREATE_URL_NAME
    ),
    path(
        'itempedido/<int:pk>/',
        item_pedido.Detail.as_view(),
        name=conf.ITEMPEDIDO_DETAIL_URL_NAME
    ),
    path(
        'itempedido/<int:pk>/update/',
        item_pedido.Update.as_view(),
        name=conf.ITEMPEDIDO_UPDATE_URL_NAME
    ),
    path(
        'itempedido/<int:pk>/delete/',
        item_pedido.Delete.as_view(),
        name=conf.ITEMPEDIDO_DELETE_URL_NAME
    ),
    path(
        'itempedido/list/json/',
        item_pedido.ItemPedidoListJson.as_view(),
        name=conf.ITEMPEDIDO_LIST_JSON_URL_NAME
    )
]

urlpatterns += api_urlpatterns
from app.views import orcamento

urlpatterns += [
    # orcamento
    path(
        'orcamento/',
        orcamento.List.as_view(),
        name=conf.ORCAMENTO_LIST_URL_NAME
    ),
    path(
        'orcamento/full/',
        orcamento.ListFull.as_view(),
        name='ORCAMENTO_list_full'
    ),
    path(
        'orcamento/create/',
        orcamento.Create.as_view(),
        name=conf.ORCAMENTO_CREATE_URL_NAME
    ),
    path(
        'orcamento/<int:pk>/',
        orcamento.Detail.as_view(),
        name=conf.ORCAMENTO_DETAIL_URL_NAME
    ),
    path(
        'orcamento/<int:pk>/update/',
        orcamento.Update.as_view(),
        name=conf.ORCAMENTO_UPDATE_URL_NAME
    ),
    path(
        'orcamento/<int:pk>/delete/',
        orcamento.Delete.as_view(),
        name=conf.ORCAMENTO_DELETE_URL_NAME
    ),
    path(
        'orcamento/list/json/',
        orcamento.OrcamentoListJson.as_view(),
        name=conf.ORCAMENTO_LIST_JSON_URL_NAME
    ),
    path(
        'orcamento/create/pedido/<int:id>/',
        orcamento.create_pedido_by_orcamento,
        name='create_pedido_by_orcamento'
    )
]

from app.views import item_orcamento

urlpatterns += [
    # item_orcamento
    path(
        'itemorcamento/',
        item_orcamento.List.as_view(),
        name=conf.ITEMORCAMENTO_LIST_URL_NAME
    ),
    path(
        'itemorcamento/full/',
        item_orcamento.ListFull.as_view(),
        name='ITEMORCAMENTO_list_full'
    ),
    path(
        'itemorcamento/create/',
        item_orcamento.Create.as_view(),
        name=conf.ITEMORCAMENTO_CREATE_URL_NAME
    ),
    path(
        'itemorcamento/<int:pk>/',
        item_orcamento.Detail.as_view(),
        name=conf.ITEMORCAMENTO_DETAIL_URL_NAME
    ),
    path(
        'itemorcamento/<int:pk>/update/',
        item_orcamento.Update.as_view(),
        name=conf.ITEMORCAMENTO_UPDATE_URL_NAME
    ),
    path(
        'itemorcamento/<int:pk>/delete/',
        item_orcamento.Delete.as_view(),
        name=conf.ITEMORCAMENTO_DELETE_URL_NAME
    ),
    path(
        'itemorcamento/list/json/',
        item_orcamento.ItemOrcamentoListJson.as_view(),
        name=conf.ITEMORCAMENTO_LIST_JSON_URL_NAME
    )
]

from app.views import dashboard

urlpatterns += [
    # dashboard
    path(
        'dashboard/',
        dashboard.DashboardView.as_view(),
        name='dashboard'
    ),
    path(
        'dashboard/list/json/',
        dashboard.DashboardListJson.as_view(),
        name='dashboard_json'
    ),
    path(
        'dashboard/top-clientes/',
        dashboard.TopClientesView.as_view(),
        name='top_clientes'
    ),
]
