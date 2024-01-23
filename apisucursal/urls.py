from django.urls import path
from . import views

urlpatterns = [
    path('v1/sucursal', views.listado_sucursal, name='listado_sucursal'),
    path('v1/sucursal/<id>', views.vista_sucursal, name='vista_sucursal'),
]