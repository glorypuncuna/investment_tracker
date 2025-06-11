from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import UserInvestment, TransactionLog
from .serializers import UserInvestmentSerializer, InvestmentCreateSerializer
from .services import InvestmentService

class InvestmentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserInvestmentListCreateView(generics.ListCreateAPIView):
    # GET /api/v1/investments/ 
    # POST /api/v1/investments/
    queryset = UserInvestment.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = InvestmentPagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-purchase_date')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InvestmentCreateSerializer
        return UserInvestmentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InvestmentSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    investment_service = InvestmentService() # Instantiate the service

    def get(self, request, *args, **kwargs):
        user = request.user
        portfolio_performance = self.investment_service.calculate_portfolio_performance(user)
        investment_insights = self.investment_service.get_investment_insights(user)

        # Combine the results from both service methods
        summary_data = {
            "portfolio_summary": portfolio_performance,
            "investment_insights": investment_insights,
        }
        return Response(summary_data, status=status.HTTP_200_OK)