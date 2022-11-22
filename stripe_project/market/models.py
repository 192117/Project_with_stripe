from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, default='usd')


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(Item)


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Discount(models.Model):
    pass


class Tax(models.Model):
    pass
