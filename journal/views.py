from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from .models import TradeLog
from .serializers import TradeLogSerializer

class TradeLogViewSet(viewsets.ModelViewSet):
    queryset = TradeLog.objects.all()
    serializer_class = TradeLogSerializer

    def get_queryset(self):
        # Deny unauthorized user.
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required")

        # Only show trades for the logged-in user
        return TradeLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


