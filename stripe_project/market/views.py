from django.views.generic import TemplateView
from rest_framework.generics import RetrieveAPIView
from .models import Item, Order
from .serializers import ItemSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
import stripe
from stripe_project.settings import STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY
from django.http import JsonResponse


class CancelView(TemplateView):
    template_name = 'cancel.html'


class SuccessView(TemplateView):
    template_name = 'success.html'


class ItemDetailView(RetrieveAPIView):
    model = Item
    serializer_class = ItemSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'market/item.html'


    def get(self, request, *args, **kwargs):
        stripe_key = STRIPE_PUBLIC_KEY
        item = Item.objects.get(id=kwargs.get('id'))
        return Response({'item': item, 'stripe_key': stripe_key})


class CartDetailView(RetrieveAPIView):
    model = Order
    serializer_class = ItemSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'market/cart.html'

    def get(self, request, *args, **kwargs):
        stripe_key = STRIPE_PUBLIC_KEY
        order = Order.objects.get(id=kwargs.get('id'))
        return Response({'order': order, 'stripe_key': stripe_key})


def buy_item(request, id):
    item = Item.objects.get(id=id)
    stripe.api_key = STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/success',
        cancel_url='http://127.0.0.1:8000/cancel',
        line_items=[
            {
                "name": item.name,
                "quantity": 1,
                "currency": "usd",
                "amount": item.price,
            },
        ],
        mode="payment",
    )
    return JsonResponse({
        'id': checkout_session.id
    })


def buy_order(request, id):
    order = Order.objects.get(id=id)
    stripe.api_key = STRIPE_SECRET_KEY
    items = []
    total = 0
    for item in order.items.all():
        items.append({
                "name": item.name,
                "quantity": 1,
                "currency": "usd",
                "amount": item.price,
            })
        total += item.price
    checkout_session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/success',
        cancel_url='http://127.0.0.1:8000/cancel',
        line_items=items,
        mode="payment",
    )
    return JsonResponse({
        'id': checkout_session.id
    })
