from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name', 'description', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'items')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('value',)
    search_fields = ('value', 'order')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('value',)
    search_fields = ('value', 'order')
