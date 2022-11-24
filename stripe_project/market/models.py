from django.db import models
import requests
from stripe_project.settings import STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY, STRIPE_URL


class AbstractItem(models.Model):
    ''' Abstract models for Item. AbstractItem contains attributes class with Stripe's information. '''
    stripe_id = models.CharField(
        verbose_name='ID позиции в Stripe',
        max_length=100
    )
    price_usd_id = models.CharField(
        verbose_name='ID цены в долларах в Stripe',
        max_length=100
    )
    price_eur_id = models.CharField(
        verbose_name='ID цены в евро в Stripe',
        max_length=100
    )


    class Meta:
        abstract = True


class AbstractDiscountTax(models.Model):
    ''' Abstract models for Discount and Tax. AbstractDiscountTax contains attributes class with Stripe's information
    for Tax and Discount. '''
    stripe_usd_id = models.CharField(
        verbose_name='ID usd в Stripe',
        max_length=100,
        null=True,
        blank=True
    )
    stripe_eur_id = models.CharField(
        verbose_name='ID eur в Stripe',
        max_length=100,
        null=True,
        blank=True
    )
    stripe_tax_id = models.CharField(
        verbose_name='ID tax в Stripe',
        max_length=100,
        null=True,
        blank=True
    )


    class Meta:
        abstract = True


class Item(AbstractItem):
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
    price_usd = models.PositiveIntegerField(
        verbose_name='Стоимость в центах (дефолтная стоимость позиции)',
        help_text='Введите стоимость позиции в центах',
        default=100
    )
    price_eur = models.PositiveIntegerField(
        verbose_name='Стоимость в евроцентах',
        help_text='Введите стоимость позиции в евроцентах',
        default=100
    )


    def save(self, *args, **kwargs):
        ''' Create Product and Price in Stripe when save instance in database. '''
        data_item = {
            'name': self.name, # The product’s name, meant to be displayable to the customer.
            'description': self.description, # The product’s description, meant to be displayable to the customer.
        }
        headers = {"Authorization": f"Bearer {STRIPE_SECRET_KEY}"}
        if not self.id:
            self.stripe_id = \
                requests.post(STRIPE_URL+'/v1/products', data=data_item, headers=headers).json()['id']
            data_usd = {'currency': 'usd', # Three-letter ISO currency code
                        'product': self.stripe_id, # The ID of the product this price is associated with.
                        'unit_amount': self.price_usd} # The unit amount in cents to be charged.
            data_eur = {'currency': 'eur', # Three-letter ISO currency code
                        'product': self.stripe_id, # The ID of the product this price is associated with.
                        'unit_amount': self.price_eur} # The unit amount in cents to be charged.
            self.price_usd_id = requests.post(STRIPE_URL+'/v1/prices', data=data_usd, headers=headers).json()['id']
            self.price_eur_id = requests.post(STRIPE_URL+'/v1/prices', data=data_eur, headers=headers).json()['id']
        requests.post(STRIPE_URL + f'/v1/products/{self.stripe_id}', data={'default_price': self.price_usd_id}, headers=headers)
        super().save(*args, **kwargs)


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


class Discount(AbstractDiscountTax):
    value_usd = models.IntegerField(
        verbose_name='Скидка в центах',
        help_text='Введите скидку',
        default=0
    )
    value_eur = models.IntegerField(
        verbose_name='Скидка в евроцентах',
        help_text='Введите скидку',
        default=0
    )
    order = models.ForeignKey(
        Order,
        verbose_name='Корзина',
        help_text="Выберите корзину из списка. В случае отсутствия необходимой корзины, добавьте её в 'Корзины'",
        on_delete=models.CASCADE
    )


    def save(self, *args, **kwargs):
        ''' Create Coupoun in Stripe when save instance in database. '''
        data_usd = {
            'duration': 'forever', # Describes how long a customer who applies this coupon will get the discount.
            'amount_off': self.value_usd, # Amount that will be taken off the subtotal of any invoices for this customer.
            'currency': 'usd' # Three-letter ISO currency code
        }
        data_eur = {
            'duration': 'forever', # Describes how long a customer who applies this coupon will get the discount.
            'amount_off': self.value_eur, # Amount that will be taken off the subtotal of any invoices for this customer.
            'currency': 'eur' # Three-letter ISO currency code
        }
        headers = {"Authorization": f"Bearer {STRIPE_SECRET_KEY}"}
        if not self.id:
            self.stripe_usd_id = \
                requests.post(STRIPE_URL + '/v1/coupons', data=data_usd, headers=headers).json()['id']
            self.stripe_eur_id = \
                requests.post(STRIPE_URL + '/v1/coupons', data=data_eur, headers=headers).json()['id']
        super().save(*args, **kwargs)


    def __str__(self):
        return f'Скидка для {self.order.name}'


    class Meta:
        verbose_name = 'Cкидка'
        verbose_name_plural = 'Скидки'
        ordering = ['-id']


class Tax(AbstractDiscountTax):
    ''' Create Tax_rate in Stripe when save instance in database. '''
    value = models.DecimalField(
        verbose_name='Налог проценты',
        help_text='Введите налог',
        max_digits=5,
        decimal_places=2,
        max_length=100.00,
    )
    order = models.ForeignKey(
        Order,
        verbose_name='Корзина',
        help_text="Выберите корзину из списка. В случае отсутствия необходимой корзины, добавьте её в 'Корзины'",
        on_delete=models.CASCADE
    )


    def save(self, *args, **kwargs):
        data = {
            'inclusive': True, # This specifies if the tax rate is inclusive or exclusive.
            'percentage': self.value, # This represents the tax rate percent out of 100.
            'display_name': 'Sales tax' # The display name of the tax rates as it will appear to your customer.
        }
        headers = {"Authorization": f"Bearer {STRIPE_SECRET_KEY}"}
        if not self.id:
            self.stripe_tax_id = \
                requests.post(STRIPE_URL + '/v1/tax_rates', data=data, headers=headers).json()['id']
        super().save(*args, **kwargs)


    def __str__(self):
        return f'Налог для {self.order.name}'


    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'
        ordering = ['-id']
