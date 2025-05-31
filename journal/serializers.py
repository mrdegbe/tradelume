from rest_framework import serializers
from .models import TradeLog

class TradeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeLog
        fields = '__all__'
        read_only_fields = ['user']  # ✅ User is set automatically
