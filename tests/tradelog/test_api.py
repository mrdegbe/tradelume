# tests/tradelog/test_api.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from journal.models import TradeLog

@pytest.mark.django_db
class TestTradeLogAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123")
        response = self.client.post("/api/token/", {"username": "testuser", "password": "password123"})
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_trade(self):
        data = {
            "pair": "GBPUSD",
            "direction": "SELL",
            "entry_price": 1.2500,
            "exit_price": 1.2400,
            "stop_loss": 1.2600,
            "take_profit": 1.2300,
            "notes": "Test short trade",
        }
        response = self.client.post("/api/trades/", data)
        assert response.status_code == 201
        assert response.data["pair"] == "GBPUSD"

    def test_get_trade_list(self):
        TradeLog.objects.create(
            user=self.user,
            pair="USDJPY",
            direction="BUY",
            entry_price=130.5,
            exit_price=131.0,
        )
        response = self.client.get("/api/trades/")
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_update_trade(self):
        trade = TradeLog.objects.create(
            user=self.user,
            pair="USDCHF",
            direction="BUY",
            entry_price=0.9000,
            exit_price=0.9100,
        )
        data = {"exit_price": 0.9200}
        response = self.client.patch(f"/api/trades/{trade.id}/", data)
        assert response.status_code == 200
        assert float(response.data["exit_price"]) == 0.9200

    def test_delete_trade(self):
        trade = TradeLog.objects.create(
            user=self.user,
            pair="AUDUSD",
            direction="SELL",
            entry_price=0.7000,
            exit_price=0.6900,
        )
        response = self.client.delete(f"/api/trades/{trade.id}/")
        assert response.status_code == 204
        assert TradeLog.objects.count() == 0
