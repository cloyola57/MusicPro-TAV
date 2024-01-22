
import logging
from pyexpat.errors import messages
from smtplib import SMTPResponseException
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from store.models.orders import Order
from store.middlewares.auth import auth_middleware
from .models import TransbankIntegration
from store.templatetags.cart import total_cart_price
import requests
from django.http import JsonResponse
from django.http import HttpResponse
import json



class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'orders.html', {'orders': orders})


def index(request):
    return render(request, 'index.html')


def realizar_pago(request):
    # Configura las credenciales adecuadas
    api_key = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
    commerce_code = "597055555532"

    transbank = TransbankIntegration(api_key=api_key, commerce_code=commerce_code)

    # Obtén los productos y el carrito
    cart = request.session.get('cart')
    product_ids = list(cart.keys())
    products = Products.get_products_by_id(product_ids)

    # Configura los detalles de la transacción
    amount = total_cart_price(products, cart)  # Monto en pesos
    order_id = "123456"  # Número de orden único
    success_url = "http://127.0.0.1:8000/exito"  # Actualiza con tu URL real
    

    # Crea la transacción
    transaction_result = transbank.create_transaction(amount, order_id, success_url)

    # Muestra la URL de pago en la consola (puedes cambiar esto según tus necesidades)
    print("URL de pago:", transaction_result)

    # Puedes pasar la URL de pago a la plantilla o redireccionar al usuario a esta URL
    return render(request, 'realizar_pago.html', {'url_pago': transaction_result['url'], 'token': transaction_result['token']})

def exito(request):
    return render(request, 'exito.html')

def error(request):
    return render(request, 'error.html')


# Get para bodega
def bodega(request):
    url='https://musicpro.bemtorres.win/api/v1/bodega/producto'
    response=requests.get(url)
    productos=response.json()
    context={
        "productos":productos['productos']
    }
    return render(request, 'bodega.html', context)



def post_bodega(request):
    if request.method == 'POST':
        # Obtiene los datos del formulario
        datos = {
            'nombre_empresa': request.POST.get('nombre_empresa'),
            'direccion_empresa': request.POST.get('direccion_empresa'),
            'productos': {
                "id_producto": request.POST.get('id_producto'),
                "cantidad": request.POST.get('cantidad')
            }
        }

        # URL de la API
        url = 'https://musicpro.bemtorres.win/api/v1/bodega/solicitud'

        # Encabezados de la solicitud
        headers = {
            'accept': 'application/json',
            'Content-Type': 'multipart/form-data',
            'X-CSRF-TOKEN': ''  # Reemplaza con tu token CSRF
        }

        try:
            # Realiza la solicitud POST
            respuesta = requests.post(url, json=datos, headers=headers)
            respuesta.raise_for_status()  # Lanza una excepción en caso de error HTTP

            # Procesa la respuesta del servidor si es necesario
            contenido_respuesta = respuesta.text

            # Devuelve una respuesta al cliente (puede ser HTML, JSON, etc.)
            return HttpResponse(f'{contenido_respuesta}')

        except requests.exceptions.RequestException as e:
            # Maneja errores de solicitud
            return HttpResponse(f'Error en la solicitud POST: {e}', status=500)

    # Si la solicitud no es un POST, renderiza el formulario o la página inicial
    return render(request, 'post_bodega.html')

#def transporte(request):
 #   url='https://musicpro.bemtorres.win/api/v1/transporte/seguimiento/{}'#70546MUSICPRO857966
  #  response=requests.get(url)
   # productos=response.json()
  #  context={
  #      "productos":productos['productos']
   # }
   # return render(request, 'bodega.html', context)

#def transporte(request, codigo_seguimiento):
 #   url = 'https://musicpro.bemtorres.win/api/v1/transporte/seguimiento/{}'.format(codigo_seguimiento)
  #  response = requests.get(url)
   # productos = response.json()
    #context = {
     #   "productos": productos['productos']
    #}
    #return render(request, 'bodega.html', context)

#Vista seguimiento
def seguimiento(request): #70546MUSICPRO857966
    if request.method == "POST":
        codigo_seguimiento = request.POST.get("codigo_seguimiento")
        dos_primeros_caracteres = codigo_seguimiento[:2]
        if dos_primeros_caracteres == 'JV':
            try:
                response = requests.get(f'https://musicpro.bemtorres.win/api/v1/transporte/seguimiento/{codigo_seguimiento}')
                print(codigo_seguimiento)
                print(response)
                response.raise_for_status()  # Lanza una excepción si hay un error HTTP en la respuesta
                data = response.json()
                print(data)
                return render(request, 'seguimiento.html', {
                    "estado": data['estado'],
                    "direccion_origen": data['direccion_origen'],
                    "direccion_destino": data['direccion_destino'],
                    "response": response,
                })
            except requests.exceptions.ConnectionError as e:
                error_msg = f'Error de conexión: {e}'
                logging.error(error_msg)  # Registra el error en el sistema de registro
                mensaje_error = 'Error de conexión. Por favor, intenta nuevamente más tarde.'
                messages.success(request, 'Error al intentar seguir pedido')
            except requests.exceptions.HTTPError as e:
                error_msg = f'Error HTTP: {e}'
                logging.error(error_msg)
                mensaje_error = 'Error HTTP. Por favor, intenta nuevamente más tarde.'
                messages.success(request, 'Error al intentar seguir pedido')
            except Exception as e:
                error_msg = f'Error en la solicitud: {e}'
                logging.error(error_msg)
                mensaje_error = 'Error en la solicitud. Por favor, intenta nuevamente más tarde.'
                messages.success(request, 'Error al intentar seguir pedido')
                context = {
                    "error": mensaje_error
                }
            return render(request, 'seguimiento.html', context)
        else:
            try:
                response = requests.get(f'https://musicpro.bemtorres.win/api/v1/transporte/seguimiento/{codigo_seguimiento}')
                response.raise_for_status()  # Lanza una excepción si hay un error HTTP en la respuesta
                data = response.json()
                if 'status' in data:
                    status = data['status']
                    result = data.get('result', {})
                    solicitud = result.get('solicitud', {})
                    return render(request, 'seguimiento.html', {
                        "status": status,
                        "result": result,
                        "solicitud": solicitud
                    })
                else:
                    mensaje_error = 'Datos incorrectos en la respuesta.'
            except requests.exceptions.ConnectionError as e:
                mensaje_error = f'Error de conexión: {e}'
                messages.success(request, 'Error al intentar seguir pedido')
            except requests.exceptions.HTTPError as e:
                mensaje_error = f'Error HTTP: {e}'
                messages.success(request, 'Error al intentar seguir pedido')
            except Exception as e:
                mensaje_error = f'Error en la solicitud: {e}'
                messages.success(request, 'Error al intentar seguir pedido')
            return render(request, 'seguimiento.html', {'error': mensaje_error})
    else:
        return render(request, 'seguimiento.html')
    

def post_transporte(request):
    if request.method == 'POST':
        data = {
            'persona_origen': request.POST.get('persona_origen'),
            'direccion_origen': request.POST.get('direccion_origen'),
            'persona_destino': request.POST.get('persona_destino'),
            'direccion_destino': request.POST.get('direccion_destino'),
            'descripcion': request.POST.get('descripcion'),
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post('http://10.155.61.4:8000/api/v1/solicitud', data=json.dumps(data), headers=headers)
        # Maneja la respuesta aquí si es necesario

        # Redirige a una nueva página después de la solicitud
        return redirect('post_transporte')

    # Si la solicitud no es POST, renderiza la página actual
    return render(request, 'post_transporte.html')




