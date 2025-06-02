from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.trades import TradeLogViewSet

router = DefaultRouter()
router.register(r'trades', TradeLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
