from django.urls import path
from django.contrib import admin
from django.urls import include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    ItemDetailView,
    CheckoutView,
    ShopView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView

)

from . import views

app_name = 'core'

urlpatterns = [
  
  # ✅ ensures / works

    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('inner-page/', innerpage, name='innerpage'),
    path('portfolio_detail/<int:pk>/', port_data, name='portfolio_detail'),
    path('about/', about, name='about'),
    path('photography/', views.photography, name='photography'),
    path('reservation/', views.reservation, name='reservation'),
    path('services/', services, name='services'),
    path('portfolio/', port, name='port'),
    path('contact/', contact, name='contact'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('pay/', views.pay, name ='pay' ),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail')
]


