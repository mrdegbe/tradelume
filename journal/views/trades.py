from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from journal.models import TradeLog
from journal.serializers import TradeLogSerializer

class TradeLogViewSet(viewsets.ModelViewSet):
    queryset = TradeLog.objects.all()
    serializer_class = TradeLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TradeLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def perform_update(self, serializer):
    #     serializer.save(user=self.request.user)


