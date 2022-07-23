from django.db import models
from django.contrib.auth.models import User


class Currency(models.Model):
    name = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categorys'
    )
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='transactions',
    )

    def __str__(self):
        return f'{self.amount} {self.currency.code} {self.date}'
