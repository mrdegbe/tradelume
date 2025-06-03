from django.db import models
from django.contrib.auth.models import User

class TradeLog(models.Model):
    TRADE_DIRECTIONS = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pair = models.CharField(max_length=10)
    direction = models.CharField(max_length=4, choices=TRADE_DIRECTIONS)
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    exit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stop_loss = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    take_profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def profit(self):
        if self.entry_price is not None and self.exit_price is not None:
            return self.exit_price - self.entry_price
        return None

    def __str__(self):
        return f"{self.user.username} - {self.pair} ({self.direction})"

