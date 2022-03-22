from ..mpesa import mpesa
from rest_framework.decorators import api_view
from rest_framework import permissions
from django.contrib.auth import get_user_model
import re
from rest_framework import status
from rest_framework.response import Response
import json
from .. import models
from markets import models as markets_models

# referencing the custom user model
User = get_user_model()

phone_regex = r'^\+?1?\d{9,14}$'

@api_view(['POST'])
def pay_with_mpesa(request):
    phone_number = request.POST.get('phone_number', '')
    amount = int(request.POST.get('amount', 0))
    recepient = int(request.POST.get('recepient', 0))
    project = int(request.POST.get('project', 0))
    if phone_number and amount and recepient:
        if amount > 0:
            if re.fullmatch(phone_regex,phone_number):
                sender = request.user.pk
                response = mpesa.pay_with_mpesa(phone_number,amount, sender, recepient, project)
                if status.is_success(response.status_code):
                    message = {
                        'status': True,
                        'message':["Payment request sent sucessfully"],
                        'details':[response.json()]
                        }
                    return Response(message, status=status.HTTP_200_OK)
                else:
                    message = {
                        'status': False,
                        'message':["Something went wrong try again later"],
                        'details':[response.json()]
                        }
                    return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                message = {'phone_number': ['The phone number you provided is not valid']}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'amount': ['Enter an amount that is larger than 0']}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        message = {
            'phone_number': ['This field is required'],
            'amount': ['This field is required'],
            'recepient':['This field is required']
            }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def settle_mpesa_payment(request):
    phone_number = request.POST.get('phone_number', '')
    amount = int(request.POST.get('amount', 0))
    if phone_number and amount:
        if amount > 0:
            if re.fullmatch(phone_regex,phone_number):
                response = mpesa.settle_payment(phone_number, amount)
                if status.is_success(response.status_code):
                    # TO DO: Update this transaction in db
                    # TO DO: Update project details to include payment details
                    message = {
                        'status': True,
                        'message':["Payment sent sucessfully"],
                        'details':[response.json()]
                        }
                    return Response(message, status=status.HTTP_200_OK)
                else:
                    message = {
                        'status': False,
                        'message':["Something went wrong try again later"],
                        'details':[response.json()]
                        }
                    return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                message = {'phone_number': ['The phone number you provided is not valid']}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'amount': ['Enter an amount that is larger than 0']}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        message = {
            'phone_number': ['This field is required'],
            'amount': ['This field is required']
            }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

def get_index(array,key,value):
    for index, element in enumerate(array):
        if element[key] == value:
            return index

@api_view(['POST'])
def pay_with_mpesa_response(request, sender_pk, recepient_pk, project_pk):
    """
        When user innitiates the pay with mpesa stk push api Mpesa
        will send a response to our callback url with the status of the payment
    """
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    status_code = int(mpesa_payment['Body']['stkCallback']['ResultCode'])
    if status_code == 0:
        sender = User.objects.filter(pk=int(sender_pk))
        recepient = User.objects.filter(pk=int(recepient_pk))
        project = markets_models.Project.objects.filter(pk=project_pk)

        if sender.exists() and recepient.exists() and project.exists():
            # 0 means payment was processed successfully
            amount_index = get_index(mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'], "Name", "Amount")
            receipt_index = get_index(mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'], "Name", "MpesaReceiptNumber")
            
            instance = models.TransactionReceipt.objects.create(
                project = project.first(),
                amount = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][amount_index]['Value'],
                payment_method = 'MPESA',
                description = f'Payment for: {project.first().requested_service.service_name}',
                reference = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][receipt_index]['Value'],
                sender = sender.first(),
                recepient = recepient.first()
            )
            context = {
                "status": True,
                "message": "Payment sent to escrow sucessfully",
                "details": [mpesa_payment['Body']['stkCallback']]
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "status": False,
                "message": "The recepient or project you provided was not found",
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    else:
        # Something went wrong or paymetn was cancelled by the user
        message = {
        "status": False,
        "message": "Payment not processed",
        "details": [mpesa_payment['Body']['stkCallback']]
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)