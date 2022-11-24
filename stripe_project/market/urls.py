from django.urls import path
from .views import ItemDetailView, buy_item, CancelView, SuccessView, buy_order, CartDetailView


urlpatterns = [
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('item/<int:id>/', ItemDetailView.as_view(), name='item_detail'),
    path('buy/<int:id>/<str:currency>/', buy_item, name='buy_item'),
    path('buy_cart/<int:id>/<str:currency>/', buy_order, name='buy_cart'),
    path('cart/<int:id>/', CartDetailView.as_view(), name='cart_detail'),
]
