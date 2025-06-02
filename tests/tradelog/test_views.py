from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class TradeLogViewSetPermissionTests(APITestCase):
    def test_unauthenticated_user_cannot_access_tradelogs(self):
        url = reverse('tradelog-list')  # Adjust if you’re using a router with different naming
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
