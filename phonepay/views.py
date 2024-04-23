from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from utils import calculate_sha256_string, base64_encode, response_data

import os  

class PhonePePaymentView(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'INR')  
        mobile_number = request.data.get('phone_number')
        email = request.data.get('email')

        if not all([order_id, amount]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = round(float(amount) * 100)  # Convert amount to paisa
        except ValueError:
            return Response({'error': 'Invalid amount format'}, status=status.HTTP_400_BAD_REQUEST)

        MAINPAYLOAD = {
            "merchantId": "PGTESTPAYUAT",
            "merchantTransactionId": order_id,
            "merchantUserId": "MUID123",
            "amount": amount,
            "redirectUrl": "http://127.0.0.1:8000/phonepay/return-to-me/",
            "redirectMode": "POST",
            "callbackUrl": "http://127.0.0.1:8000/phonepay/return-to-me/",
            "mobileNumber": mobile_number,
            "email": email,
            "paymentInstrument": {
                "type": "PAY_PAGE"
            }
        }

        INDEX = "1"
        ENDPOINT = "/pg/v1/pay"
        SALTKEY = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"

        base64String = base64_encode(MAINPAYLOAD)
        mainString = base64String + ENDPOINT + SALTKEY;
        sha256Val = calculate_sha256_string(mainString)
        checkSum = sha256Val + '###' + INDEX;

        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': checkSum,
            'accept': 'application/json',
        }
        json_data = {
            'request': base64String,
        }

        response = requests.post('https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay', headers=headers, json=json_data)
        responseData = response.json()

        return Response(response_data(False, "Redirected to Phonepay payment screen.",
            responseData['data']['instrumentResponse']['redirectInfo']['url']), status=status.HTTP_200_OK)
