from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.trades import TradeLogViewSet
from .views import analytics

router = DefaultRouter()
router.register(r'trades', TradeLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("analytics/", analytics.get_analytics, name="analytics"),
]
