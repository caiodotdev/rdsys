import datetime
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from djmoney.money import Money

from app.models import Cliente, Vendedor, Item, FormaPagamento, StatusPedido, Pedido, ItemPedido


class Command(BaseCommand):
    help = 'Starting Project'

    def handle(self, *args, **options):
        self.create_clients()
        self.create_vendedores()
        self.create_items()
        self.create_forma_pgto()
        self.create_status_pedido()
        self.create_pedidos()
        self.stdout.write(self.style.SUCCESS('Successfully starting project'))

    def create_pedidos(self):
        status = [status for status in StatusPedido.objects.all()]
        pgtos = [forma for forma in FormaPagamento.objects.all()]
        num_itens = [i for i in range(10)]
        items = [item for item in Item.objects.all()]
        dia = [i for i in range(1, 28)]
        mes = [i for i in range(1, 13)]
        ano = [i for i in range(2021, 2023)]
        for cliente in Cliente.objects.all():
            for vendedor in Vendedor.objects.all():
                pedido = Pedido()
                pedido.status = random.choice(status)
                pedido.cliente = cliente
                pedido.vendedor = vendedor
                pedido.descricao = 'Caution: this setting also affects the initial migration of the exchange plugin, so changing it after running the initial migration has no effect. (You would need to manage migrate exchange zero and migrate again if you want to change it).'
                pedido.forma_pagamento = random.choice(pgtos)
                pedido.save()
                for i in range(random.choice(num_itens)):
                    item_pedido = ItemPedido()
                    item_choosed = random.choice(items)
                    qtd_selected = random.choice(num_itens)
                    item_pedido.item = item_choosed
                    item_pedido.pedido = pedido
                    item_pedido.qtd = qtd_selected
                    item_pedido.valor_total = item_choosed.valor_unitario * qtd_selected
                    item_pedido.save()
                valor_total_pedido = 0
                for item in pedido.itempedido_set.all():
                    valor_total_pedido = valor_total_pedido + item.valor_total
                pedido.valor_total = valor_total_pedido
                pedido.criado_em = datetime.datetime(random.choice(ano),
                                                     random.choice(mes), random.choice(dia)).date().strftime('%Y-%m-%d')
                pedido.save()

    def create_status_pedido(self):
        aberto = StatusPedido()
        aberto.nome_status = 'Aberto'
        aberto.save()
        producao = StatusPedido()
        producao.nome_status = 'Em Produção'
        producao.save()
        finalizado = StatusPedido()
        finalizado.nome_status = 'Finalizado'
        finalizado.save()
        pgto_pendente = StatusPedido()
        pgto_pendente.nome_status = 'Pagamento Pendente'
        pgto_pendente.save()

    def create_forma_pgto(self):
        cartao = FormaPagamento()
        cartao.tipo = 'Cartao Credito'
        cartao.save()
        pix = FormaPagamento()
        pix.tipo = 'PIX'
        pix.save()
        dinheiro = FormaPagamento()
        dinheiro.tipo = 'dinheiro'
        dinheiro.save()

    def create_items(self):
        for i in range(25):
            item = Item()
            item.descricao = 'Banner 10x' + str(i) + ' na folha x100'
            item.preco_custo = Money(float(i) + 0.99, 'BRL')
            item.valor_unitario = Money(float(i) + 0.99, 'BRL')
            item.save()

    def create_vendedores(self):
        for i in range(5):
            user = User.objects.create_superuser('vendedor' + str(i), 'v' + str(i) + '@ex.com', 'admin123', **{
                'first_name': 'Vendedor ' + str(i),
                'last_name': 'Silva'
            })
            vendedor = Vendedor()
            vendedor.user = user
            vendedor.save()

    def create_clients(self):
        tipo_cliente = ['Novo', 'Normal']
        endereco_cliente = ['Rua Claudio Bezerra de Lima',
                            'Rua Getulio Vargas',
                            'Rua getulio cavalcanti',
                            'rua maria da guia muniz albuquerque']
        cpfs = ['341.626.820-20',
                '535.862.050-82',
                '757.431.520-55',
                '541.141.340-00',
                '585.992.040-76']
        cnpjs = ['48.034.131/0001-16',
                 '67.429.769/0001-09',
                 '55301069000147',
                 '93.304.918/0001-05']
        for i in range(65):
            cliente = Cliente()
            cliente.nome = 'Cliente ' + str(i)
            cliente.endereco = random.choice(endereco_cliente)
            cliente.numero = '541'
            cliente.tipo = random.choice(tipo_cliente)
            cliente.email = 'caio@' + str(i) + '.com'
            cliente.cpf = random.choice(cpfs)
            cliente.cnpj = random.choice(cnpjs)
            cliente.bairro = ''
            cliente.cidade = 'Campina Grande'
            cliente.cep = ''
            cliente.estado = 'PB'
            cliente.instagram = '@cliente_' + str(i)
            cliente.telefone = '83997445211'
            cliente.save()
