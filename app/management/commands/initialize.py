from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from app.models import Vendedor, FormaPagamento, StatusPedido


class Command(BaseCommand):
    help = 'Starting Project'

    def handle(self, *args, **options):
        self.create_vendedores()
        self.create_forma_pgto()
        self.create_status_pedido()
        self.stdout.write(self.style.SUCCESS('Successfully starting project'))

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
        cartaoD = FormaPagamento()
        cartaoD.tipo = 'Débito'
        cartaoD.save()
        pix = FormaPagamento()
        pix.tipo = 'PIX'
        pix.save()
        dinheiro = FormaPagamento()
        dinheiro.tipo = 'Dinheiro'
        dinheiro.save()
        dinheiro = FormaPagamento()
        dinheiro.tipo = 'TED'
        dinheiro.save()

    def create_vendedores(self):
        user = User.objects.create_superuser('renan', '', 'Admin123!', **{
            'first_name': 'Renan',
            'last_name': 'Dantas'
        })
        vendedor = Vendedor()
        vendedor.user = user
        vendedor.save()
        user2 = User.objects.create_superuser('anthony', '', 'Admin123!', **{
            'first_name': 'Anthony',
            'last_name': 'Ferreira'
        })
        vendedor = Vendedor()
        vendedor.user = user2
        vendedor.save()
        User.objects.create_superuser('caio', '', 'oficinag3', **{
            'first_name': 'Caio',
            'last_name': 'Marinho'
        })
