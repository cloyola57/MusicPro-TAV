from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from store.models import Products
from .serializers import ProductsSerializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status

@csrf_exempt #para que no pida tocken de acceso
@api_view(['GET','POST']) #solo acepte perticiones GET
def listado_sucursal(request):
    if request.method == 'GET':
        solicitud = Products.objects.all()
        serializer = ProductsSerializers(solicitud, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductsSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
@csrf_exempt #para que no pida tocken de acceso
@api_view(['GET','PUT','DELETE']) #solo acepte perticiones GET
def vista_sucursal(request, id):
    if request.method == 'GET':
        try:
            order = Products.objects.get(id=id)
        except Products.DoesNotExist:
            return Response(status=status.HTPP_404_NOT_FOUND)
        serializer = ProductsSerializers(order)
        return Response(serializer.data)
    elif request.method == 'PUT':
        try:
            order = Products.objects.get(id=id)
        except Products.DoesNotExist:
            return Response(status=status.HTPP_404_NOT_FOUND)
        data = JSONParser().parse(request)
        serializer = ProductsSerializers(order, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.data, status=status.HTPP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            order = Products.objects.get(id=id)
        except Products.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)