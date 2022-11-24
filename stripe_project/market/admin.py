from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_usd', 'price_eur')
    search_fields = ('name', 'price_usd', 'price_eur')
    exclude = ('stripe_id', 'price_usd_id', 'price_eur_id')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'items')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('value_usd', 'value_eur', 'order')
    search_fields = ('value_usd', 'value_eur', 'order')
    exclude = ('stripe_usd_id', 'stripe_eur_id', 'stripe_tax_id')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('value', 'order')
    search_fields = ('value', 'order')
    exclude = ('stripe_usd_id', 'stripe_eur_id', 'stripe_tax_id')
