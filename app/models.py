from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator, MaxMoneyValidator
# Create your models here.
from djmoney.money import Money


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)


TIPO_CLIENTE = (
    ('Novo', 'Novo'),
    ('Normal', 'Normal')
)


class Cliente(TimeStamped):
    nome = models.CharField(max_length=255, blank=True, null=True)
    cep = models.CharField(max_length=255, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=255, blank=True, null=True)
    cpf = models.CharField(max_length=255, blank=True, null=True)
    cnpj = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    tipo = models.CharField(max_length=255, choices=TIPO_CLIENTE, blank=True, null=True,
                            default='Novo')

    def __str__(self):
        return "%s" % self.nome


class Vendedor(TimeStamped):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.user.first_name


class FormaPagamento(TimeStamped):
    tipo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % self.tipo


class StatusPedido(TimeStamped):
    nome_status = models.CharField(max_length=255, blank=True, null=True)
    cor = models.CharField(max_length=255, blank=True, null=True, choices=(
        ('default', 'Padrao'),
        ('info', 'Azul Claro'),
        ('primary', 'Azul Escuro'),
        ('success', 'Verde'),
        ('danger', 'Vermelho'),
        ('warning', 'Amarelo'),
    ))

    def __str__(self):
        return "%s" % self.nome_status


class Pedido(TimeStamped):
    vendedor = models.ForeignKey(Vendedor, blank=True, null=True, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, blank=True, null=True, on_delete=models.CASCADE)
    forma_pagamento = models.ForeignKey(FormaPagamento, blank=True, null=True, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusPedido, blank=True, null=True, on_delete=models.CASCADE)
    descricao = models.TextField(blank=True, null=True)
    valor_total = MoneyField(decimal_places=2, max_digits=10,
                             default=Money(0, 'BRL'),
                             validators=[
                                 MinMoneyValidator(0),
                                 MaxMoneyValidator(100000),
                             ])


class Item(TimeStamped):
    descricao = models.CharField(max_length=255, blank=True, null=True)
    preco_custo = MoneyField(decimal_places=2, max_digits=10,
                             default=Money(0, 'USD'),
                             validators=[
                                 MinMoneyValidator(0),
                                 MaxMoneyValidator(100000),
                             ])
    valor_unitario = MoneyField(decimal_places=2, max_digits=10,
                                default=Money(0, 'USD'),
                                validators=[
                                    MinMoneyValidator(0),
                                    MaxMoneyValidator(100000),
                                ])
    foto = models.URLField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.descricao


class ItemPedido(TimeStamped):
    pedido = models.ForeignKey(Pedido, blank=True, null=True, on_delete=models.CASCADE)
    qtd = models.IntegerField(default=1)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE)
    valor_total = MoneyField(decimal_places=2, max_digits=10,
                             default=Money(0, 'USD'),
                             validators=[
                                 MinMoneyValidator(0),
                                 MaxMoneyValidator(100000),
                             ])


class Orcamento(TimeStamped):
    vendedor = models.ForeignKey(Vendedor, blank=True, null=True, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, blank=True, null=True, on_delete=models.CASCADE)
    forma_pagamento = models.ForeignKey(FormaPagamento, blank=True, null=True, on_delete=models.CASCADE)
    valor_total = MoneyField(decimal_places=2, max_digits=10,
                             default=Money(0, 'BRL'),
                             validators=[
                                 MinMoneyValidator(0),
                                 MaxMoneyValidator(100000),
                             ])


class ItemOrcamento(TimeStamped):
    orcamento = models.ForeignKey(Orcamento, blank=True, null=True, on_delete=models.CASCADE)
    qtd = models.IntegerField(default=1)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE)
    valor_total = MoneyField(decimal_places=2, max_digits=10,
                             default=Money(0, 'USD'),
                             validators=[
                                 MinMoneyValidator(0),
                                 MaxMoneyValidator(100000),
                             ])
