from django.shortcuts import render, redirect
from .models import TransbankIntegration
import requests
import json

def index(request):
    return render(request, 'index.html')

def realizar_pago(request):
    # Configura las credenciales adecuadas
    api_key = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
    commerce_code = "597055555532"

    transbank = TransbankIntegration(api_key=api_key, commerce_code=commerce_code)

    # Configura los detalles de la transacción
    amount = 10000  # Monto en pesos
    order_id = "123456"  # Número de orden único
    success_url = "http://127.0.0.1:8000/exito"  # Actualiza con tu URL real
    failure_url = "http://127.0.0.1:8000/error"  # Actualiza con tu URL real

    # Crea la transacción
    transaction_result = transbank.create_transaction(amount, order_id, success_url, failure_url)

    # Muestra la URL de pago en la consola (puedes cambiar esto según tus necesidades)
    print("URL de pago:", transaction_result)

    # Puedes pasar la URL de pago a la plantilla o redireccionar al usuario a esta URL
    #return render(request, 'realizar_pago.html', {'url_pago': transaction_result})
    
    # Redirecciona al usuario a la URL de pago
    #return redirect(transaction_result['url'])
    # Redirecciona al usuario a la plataforma de pago de Transbank
    return render(request, 'realizar_pago.html', {'url_pago': transaction_result['url'], 'token': transaction_result['token']})

def exito(request):
    return render(request, 'exito.html')

def error(request):
    return render(request, 'error.html')

def bodega(request):
    url='https://musicpro.bemtorres.win/api/v1/bodega/solicitud'
    response=requests.get(url)
    productos=response.json()
    print (productos)


