from django.conf import settings
from django.db import models
from markets import models as markets_models


class TransactionReceipt(models.Model):
    TRANSACTION_STATUS = (
        ('ESCROW','escrow'),
        ('SETTLED','settled'),
        ('REFUNDED','refunded'),
    )
    PAYMENT_METHOD = (
        ('MPESA','mpesa'),
        ('CARD','card'),
    )
    project = models.ForeignKey(markets_models.Project, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(default=None)
    transaction_status = models.CharField(choices=TRANSACTION_STATUS, max_length=25, default='ESCROW')
    payment_method = models.CharField(choices=PAYMENT_METHOD,max_length=25, default='MPESA')
    description = models.TextField()
    reference = models.TextField(default=None, null=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="transaction_receipt_payment_sender", on_delete=models.SET_NULL, null=True)
    recepient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="transaction_receipt_payment_recepient", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f'{self.sender.username} - {self.amount} - to {self.sender.username}'
    
    class Meta:
        verbose_name_plural = "Transaction receipts"