
from .models import UserInvestment
from django.db.models import Sum, Avg, F, ExpressionWrapper, DecimalField, Min, Max
from decimal import Decimal
from django.utils import timezone

class InvestmentService:

    def calculate_portfolio_performance(self, user):
        # Get all active investments for the user
        investments = UserInvestment.objects.filter(user=user, is_active=True)

        # if the investments nil or empty, return default values
        if not investments.exists():
            return {
                "total_invested": Decimal('0.00'),
                "current_portfolio_value": Decimal('0.00'),
                "total_profit_loss": Decimal('0.00'),
                "total_profit_loss_percentage": Decimal('0.00'),
                "number_of_active_investments": 0,
                "best_performing_investment": None,
                "worst_performing_investment": None,
            }

        # Calculate total invested and current portfolio value
        total_invested = Decimal('0.00')
        best_performing = None
        worst_performing = None
        best_profit_loss = Decimal('-Infinity')
        worst_profit_loss = Decimal('Infinity')

        for investment in investments:
            total_invested += investment.amount_invested
            profit_loss = investment.current_value - investment.amount_invested
            if profit_loss > best_profit_loss:
                best_profit_loss = profit_loss
                best_performing = investment
            if profit_loss < worst_profit_loss:
                worst_profit_loss = profit_loss
                worst_performing = investment
            
        current_portfolio_value = investment.current_value
        total_profit_loss = current_portfolio_value - total_invested

        return {
            "total_invested": round(total_invested, 2),
            "current_portfolio_value": round(current_portfolio_value, 2),
            "total_profit_loss": round(total_profit_loss, 2),
            "number_of_active_investments": investments.count(),
            "best_performing_investment": best_performing,
            "worst_performing_investment": worst_performing,
        }

    def get_investment_insights(self, user):
        investments = UserInvestment.objects.filter(user=user, is_active=True)

        if not investments.exists():
            return {
                "average_holding_period_days": 0,
                "preferred_investment_size": Decimal('0.00'),
                "min_investment_amount": Decimal('0.00'),
                "max_investment_amount": Decimal('0.00'),
            }

        total_holding_days = 0
        average_holding_period_days = 0
        preferred_investment_size = Decimal('0.00')
        for investment in investments:
            duration_holding = timezone.now() - investment.purchase_date
            total_holding_days += duration_holding.days
            preferred_investment_size += investment.amount_invested


        if investments.count() > 0:
            average_holding_period_days = total_holding_days / investments.count()
            preferred_investment_size /= investments.count()
            
        return {
            "average_holding_period_days": round(average_holding_period_days),
            "preferred_investment_size": round(preferred_investment_size, 2),
        }