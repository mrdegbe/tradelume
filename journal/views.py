from rest_framework import viewsets
from .models import TradeLog
from .serializers import TradeLogSerializer

class TradeLogViewSet(viewsets.ModelViewSet):
    queryset = TradeLog.objects.all()
    serializer_class = TradeLogSerializer

