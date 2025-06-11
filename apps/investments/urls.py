from django.urls import path
from apps.investments.views import UserInvestmentListCreateView, InvestmentSummaryView

urlpatterns = [
    path('investments/', UserInvestmentListCreateView.as_view(), name='investment-list-and-create'),
    path('investments/summary/', InvestmentSummaryView.as_view(), name='investment-summary'),
]