from django.contrib import admin
from django.urls import path
from store.views import realizar_pago
from .views.home import Index , store
from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart, Exito
from .views.checkout import CheckOut
from .views.orders import OrderView, post_bodega, realizar_pago, bodega, seguimiento, post_transporte
from .middlewares.auth import  auth_middleware


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('realizar_pago', realizar_pago, name='realizar_pago'),
    path('exito', auth_middleware(Exito.as_view()) , name='exito'),
    path('bodega_musicpro', bodega, name='bodega'),
    path('seguimiento_musicpro', seguimiento, name='seguimiento'), 
    path('post_bodega', post_bodega,name='post_bodega' ),
    path('post_transporte', post_transporte, name='post_transporte')

]
