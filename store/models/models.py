from django.db import models

# Create your models here.
import requests

class TransbankIntegration(models.Model):
    api_key = models.CharField(max_length=255)
    commerce_code = models.CharField(max_length=255)
    
    class Meta:
        app_label = 'store'

    def create_transaction(self, amount, order_id, success_url, failure_url):
        endpoint = "/rswebpaytransaction/api/webpay/v1.2/transactions"
        url = "https://webpay3gint.transbank.cl" + endpoint

        headers = {
            "Content-Type": "application/json",
            "Tbk-Api-Key-Id": self.commerce_code,
            "Tbk-Api-Key-Secret": self.api_key,
        }

        data = {
            "buy_order": order_id,
            "session_id": order_id,
            "amount": amount,
            "return_url": success_url,
            #"final_url": failure_url,
        }

        response = requests.post(url, json=data, headers=headers)

        # Manejo básico de la respuesta
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error en la solicitud: {response.status_code}"}