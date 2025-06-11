from django.db import models
from django.contrib.auth.models import User

class UserInvestment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    asset_name = models.CharField(max_length=255)
    amount_invested = models.DecimalField(max_digits=15, decimal_places=2)
    purchase_date = models.DateTimeField()
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.asset_name}"

class TransactionLog(models.Model):
    DEPOSIT = 'DEPOSIT'
    WITHDRAWAL = 'WITHDRAWAL'
    PURCHASE = 'PURCHASE'

    TRANSACTION_TYPE = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (PURCHASE, 'Purchase'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.reference_id}"