import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from djmoney.money import Money

from app.models import Cliente, Vendedor, Item, FormaPagamento, StatusPedido, Pedido, ItemPedido


class Command(BaseCommand):
    help = 'Starting Project'

    def handle(self, *args, **options):
        Cliente.objects.all().delete()
        Vendedor.objects.all().delete()
        Item.objects.all().delete()
        FormaPagamento.objects.all().delete()
        StatusPedido.objects.all().delete()
        Pedido.objects.all().delete()
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleting all project'))
