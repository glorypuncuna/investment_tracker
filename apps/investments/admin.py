from django.contrib import admin
from apps.investments.models import UserInvestment, TransactionLog

admin.site.register(UserInvestment)
admin.site.register(TransactionLog) 