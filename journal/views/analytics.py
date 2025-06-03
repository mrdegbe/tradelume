from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from journal.models import TradeLog

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_analytics(request):
    trades = TradeLog.objects.filter(user=request.user)
    total_trades = trades.count()

    if total_trades == 0:
        return Response({
            "total_trades": 0,
            "win_rate": 0,
            "avg_rr": 0,
            "profit_factor": 0,
            "net_profit": 0,
            "average_profit": 0,  # 👈 added
            "max_drawdown": 0,
        })

    wins, losses, rr_ratios = [], [], []
    net_profit = 0
    equity_curve = []

    for trade in trades:
        # 👇 Calculate profit dynamically since there's no profit field
        profit = trade.exit_price - trade.entry_price
        net_profit += profit
        equity_curve.append(net_profit)

        if profit > 0:
            wins.append(profit)
        elif profit < 0:
            losses.append(profit)

        # 👇 R:R logic (same as before)
        risk = abs(trade.entry_price - trade.stop_loss) if trade.stop_loss else 0
        reward = abs(trade.exit_price - trade.entry_price)
        if risk > 0:
            rr_ratios.append(reward / risk)

    # 👇 Updated win rate and profit factor calculations
    win_rate = round((len(wins) / total_trades) * 100, 2)
    avg_rr = round(sum(rr_ratios) / len(rr_ratios), 2) if rr_ratios else 0
    gross_profit = sum(wins)
    gross_loss = abs(sum(losses)) or 1  # 👈 Prevent divide-by-zero
    profit_factor = round(gross_profit / gross_loss, 2)
    average_profit = round(net_profit / total_trades, 2)

    # 👉 Max drawdown calculation
    peak = equity_curve[0]
    max_dd = 0
    for equity in equity_curve:
        if equity > peak:
            peak = equity
        dd = peak - equity
        if dd > max_dd:
            max_dd = dd

    return Response({
        "total_trades": total_trades,
        "win_rate": win_rate,
        "avg_rr": avg_rr,
        "profit_factor": profit_factor,
        "net_profit": round(net_profit, 2),
        "average_profit": average_profit,
        "max_drawdown": round(max_dd, 2),
    })
