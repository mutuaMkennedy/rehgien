from tokenize import endpats
import requests
from requests.auth import HTTPBasicAuth
import re
from django.contrib.sites.models import Site
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

CONSUMER_KEY = settings.CONSUMER_KEY
CONSUMER_SECRET = settings.CONSUMER_SECRET
ACCESS_TOKEN_API_ENDPOINT = settings.ACCESS_TOKEN_API_ENDPOINT
REGISTER_URL_API_ENDPOINT = settings.REGISTER_URL_API_ENDPOINT
MPESA_EXPRESS_API_ENDPOINT = settings.MPESA_EXPRESS_API_ENDPOINT
MPESA_B2C_API_ENDPOINT = settings.MPESA_B2C_API_ENDPOINT

phone_regex = r'^\+?1?\d{9,14}$'
base_url = 'd4ee-41-80-112-95.ngrok.io'

def get_access_token():
    endpoint = ACCESS_TOKEN_API_ENDPOINT
    headers = { 
        'Authorization': 'Bearer cFJZcjZ6anEwaThMMXp6d1FETUxwWkIzeVBDa2hNc2M6UmYyMkJmWm9nMHFRR2xWOQ==' 
    }
    response = requests.request("GET", endpoint, headers = headers, auth=HTTPBasicAuth(CONSUMER_KEY,CONSUMER_SECRET)).json()
    # print(response.text.encode('utf8'))
    return response['access_token']

def register_url():
    """
    TO DO: Check on the use of this API since Other mpesa apis don't seem to require it
    """
    access_token = get_access_token()
    endpoint = REGISTER_URL_API_ENDPOINT
    headers = {
    # 'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ access_token
    }
    payload = {
        "ValidationURL":"https://" + base_url +"/apis/payments/mpesa/b2c/validate/",
        "ConfirmationURL":"https://" + base_url +"/apis/payments/mpesa/b2c/confirm/",
        "ResponseType":'Completed',
        "ShortCode":600998,
    }
    response = requests.request("POST", endpoint, headers = headers, json = payload)
    # print(response.text.encode('utf8'))
    return response

def confirm(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    print(mpesa_payment)
    pass

def validate(request):
    pass

def pay_with_mpesa(phone_number,amount,sender, recepient, project):
    """
    Function that handles sending of money from customers phone number to
    our paybill which we use as an escrow account
    """
    if re.fullmatch(phone_regex,phone_number):
        # if phone number is valid
        sender_phone_number = int('254' + phone_number[-9:])
        access_token = get_access_token()
        endpoint = MPESA_EXPRESS_API_ENDPOINT
        headers = {
        # 'Content-Type': 'application/json',
        'Authorization': 'Bearer '+ access_token
        }
        payload = {
            "BusinessShortCode": 174379,
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjIwMzA3MTU1NjM0",
            "Timestamp": "20220307155634",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": sender_phone_number,
            "PartyB": 174379,
            "PhoneNumber": sender_phone_number,
            "CallBackURL": f"https://{base_url}/apis/payments/mpesa/stkpush/pay/{sender}/{recepient}/{project}/payment_response/",
            "AccountReference": "CompanyXLTD",
            "TransactionDesc": "Payment of X" 
        }
        response = requests.request("POST", endpoint, headers = headers, json = payload)
        # print(response.text)
        return response

def settle_payment(phone_number, amount):
    """
    Function that handles sending of money from customers phone number to
    our paybill we use as an escrow account
    """
    if re.fullmatch(phone_regex,phone_number):
        # if phone number is valid
        recepient_phone_number = int('254' + phone_number[-9:])
        access_token = get_access_token()
        endpoint = MPESA_B2C_API_ENDPOINT
        headers = {
        # 'Content-Type': 'application/json',
        'Authorization': 'Bearer '+ access_token
        }
        payload = {
            "InitiatorName": "RehgienEscrowPay",
            "SecurityCredential": "l0vSM1fAEJeQEmVW0jBfOnFP4oUMrtU1A9qXHU6+HYnqDbDeLr8Jq+Vdh2d5jm1D9caXF3myZusO++SPFWtgSR0N2yDvjXimJSXzcGsP779F6Yz0gKQGTmJzCNhBI1sR9NwQ8NtjbtV8x8WloPaRMoqB6ZThTFzVTLldKMmYICeIzuGu9pv/sT7T8HUl4fVFEbZpl7ZLXzxUEv0kWJuhSqB428Tk952ihHeZ2kDO21SGPJ1Ei7ghmDRynVi5u9S38uwAb1uDhv2zqSnDwlm3zEI3citUyJTk4UJk3KF/+EiEjECQE72B2pybtouBFigQQjuRlThIDEJidDkI8wF21A==",
            "CommandID": "BusinessPayment",
            "Amount": amount,
            "PartyA": 600995,
            "PartyB": recepient_phone_number,
            "Remarks": "Test remarks",
            "QueueTimeOutURL": "https://mydomain.com/b2c/queue",
            "ResultURL": "https://mydomain.com/b2c/result",
            "Occassion": "fdf",
        }
        response = requests.request("POST", endpoint, headers = headers, json = payload)
        # print(response.text.encode('utf8'))
        return response