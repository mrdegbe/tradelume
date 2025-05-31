# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from journal.models import TradeLog
User = get_user_model()

class TradeLogTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='traderjoe', password='secret123')
        # ✅ Correct way to simulate authenticated API user
        self.client.force_authenticate(user=self.user)
        self.trade_data = {
            "pair": "EUR/USD",
            "direction": "BUY",
            "entry_price": 1.1000,
            "exit_price": 1.1200,
            "stop_loss": 1.0900,
            "take_profit": 1.1300,
            "notes": "Test trade"
        }

    def test_create_tradelog(self):
        response = self.client.post("/api/trades/", self.trade_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TradeLog.objects.count(), 1)
        self.assertEqual(TradeLog.objects.first().pair, "EUR/USD")

    def test_read_tradelog(self):
        trade = TradeLog.objects.create(user=self.user, **self.trade_data)
        response = self.client.get(f"/api/trades/{trade.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pair"], "EUR/USD")

    def test_update_tradelog(self):
        trade = TradeLog.objects.create(user=self.user, **self.trade_data)
        update_data = self.trade_data.copy()
        update_data["pair"] = "GBP/USD"
        response = self.client.put(f"/api/trades/{trade.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pair"], "GBP/USD")

    def test_delete_tradelog(self):
        trade = TradeLog.objects.create(user=self.user, **self.trade_data)
        response = self.client.delete(f"/api/trades/{trade.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TradeLog.objects.count(), 0)
