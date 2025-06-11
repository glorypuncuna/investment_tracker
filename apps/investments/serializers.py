from rest_framework import serializers
from apps.investments.models import UserInvestment, TransactionLog
from decimal import Decimal

class UserInvestmentSerializer(serializers.ModelSerializer):
    profit_loss = serializers.SerializerMethodField()
    profit_loss_percentage = serializers.SerializerMethodField()

    class Meta:
        model = UserInvestment
        fields = [
            'id', 'asset_name', 'amount_invested', 'current_value',
            'profit_loss', 'profit_loss_percentage', 'purchase_date'
        ]
        read_only_fields = ['user']

    def get_profit_loss(self, obj):
        return obj.current_value - obj.amount_invested

    def get_profit_loss_percentage(self, obj):
        if obj.amount_invested == 0:
            return Decimal('0.00')
        profit_loss = self.get_profit_loss(obj)
        percentage = (profit_loss / obj.amount_invested) * 100
        return round(percentage, 2)

class InvestmentCreateSerializer(serializers.ModelSerializer):
    profit_loss = serializers.SerializerMethodField()
    profit_loss_percentage = serializers.SerializerMethodField()

    class Meta:
        model = UserInvestment
        fields = [
            'id', 'asset_name', 'amount_invested', 'purchase_date',
            'current_value', 'profit_loss', 'profit_loss_percentage'
        ]
        read_only_fields = ['id', 'profit_loss', 'profit_loss_percentage']

    def validate_amount_invested(self, value):
        if value < 1000:
            raise serializers.ValidationError("Minimum investment amount is $1000.")
        return value

    def create(self, validated_data):
 
        user = self.context['request'].user
        validated_data['user'] = user

        if 'current_value' not in validated_data or validated_data['current_value'] is None:
            validated_data['current_value'] = validated_data['amount_invested']

        instance = UserInvestment.objects.create(**validated_data)

        TransactionLog.objects.create(
            user=user,
            transaction_type=TransactionLog.PURCHASE,
            amount=instance.amount_invested,
            reference_id=f"INVESTMENT-{instance.id}-{instance.purchase_date.strftime('%Y%m%d%H%M%S')}"
        )
        return instance

    def get_profit_loss(self, obj):
        return obj.current_value - obj.amount_invested

    def get_profit_loss_percentage(self, obj):
        if obj.amount_invested == 0:
            return Decimal('0.00')
        profit_loss = self.get_profit_loss(obj)
        percentage = (profit_loss / obj.amount_invested) * 100
        return round(percentage, 2)