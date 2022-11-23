from django.db import models


class Item(models.Model):
    class Status(models.TextChoices):
        usd = 'usd', 'Доллар'
        eur = 'eur', 'Евро'

    name = models.CharField(
        verbose_name='Имя позиции',
        help_text='Введите наименование позиции',
        max_length=100
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание позиции',
        max_length=1000
    )
    price = models.PositiveIntegerField(
        verbose_name='Стоимость в центах или евроцентах',
        help_text='Введите стоимость позиции в центах или евроцентах',
        default=100
    )
    currency = models.CharField(
        verbose_name="Валюта",
        help_text="Выберите валюту продажи",
        choices=Status.choices,
        default=Status.usd,
        max_length=5
    )


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    name = models.CharField(
        verbose_name='Имя корзины',
        help_text='Введите наименование корзины',
        max_length=100
    )
    items = models.ManyToManyField(
        Item,
        verbose_name='Позиции',
        help_text="Выберите позиции из списка. В случае отсутствия необходимой позиции, добавьте её в 'Товары'",
    )


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Discount(models.Model):
    value = models.IntegerField(
        verbose_name='Скидка',
        help_text='Введите скидку',
        default=0
    )
    order = models.ForeignKey(
        Order,
        verbose_name='Корзина',
        help_text="Выберите корзину из списка. В случае отсутствия необходимой корзины, добавьте её в 'Корзины'",
        on_delete=models.CASCADE
    )


    def __str__(self):
        return f'Скидка для {self.order.name}'


    class Meta:
        verbose_name = 'Cкидка'
        verbose_name_plural = 'Скидки'


class Tax(models.Model):
    value = models.IntegerField(
        verbose_name='Налог',
        help_text='Введите налог',
        default=0
    )
    order = models.ForeignKey(
        Order,
        verbose_name='Корзина',
        help_text="Выберите корзину из списка. В случае отсутствия необходимой корзины, добавьте её в 'Корзины'",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Налог для {self.order.name}'

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'
