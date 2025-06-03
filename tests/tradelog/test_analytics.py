import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from journal.models import TradeLog

User = get_user_model()

@pytest.mark.django_db
class TestAnalyticsAPI:
    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Sample trades
        TradeLog.objects.create(
            user=self.user,
            pair="EUR/USD",
            direction="buy",
            entry_price=1.1000,
            exit_price=1.1050,  # profit
            stop_loss=1.0950,
            take_profit=1.1100,
            notes="Nice trade"
        )
        TradeLog.objects.create(
            user=self.user,
            pair="USD/JPY",
            direction="sell",
            entry_price=110.00,
            exit_price=109.50,  # profit
            stop_loss=110.50,
            take_profit=109.00,
            notes="Smooth short"
        )
        TradeLog.objects.create(
            user=self.user,
            pair="GBP/USD",
            direction="buy",
            entry_price=1.2500,
            exit_price=1.2400,  # loss
            stop_loss=1.2450,
            take_profit=1.2600,
            notes="Bad setup"
        )

    def test_analytics_response(self):
        response = self.client.get("/api/analytics/")
        assert response.status_code == 200
        data = response.json()

        assert "total_trades" in data
        assert data["total_trades"] == 3

        assert "win_rate" in data
        assert isinstance(data["win_rate"], float)

        assert "average_profit" in data
        assert isinstance(data["average_profit"], float)

        assert "max_drawdown" in data
        assert isinstance(data["max_drawdown"], float)
