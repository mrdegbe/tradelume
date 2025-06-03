from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from journal.models import TradeLog
from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_analytics(request):
    trades = TradeLog.objects.filter(user=request.user)

    # ⏱️ Optional date filtering
    start_date = parse_date(request.query_params.get("start_date", ""))
    end_date = parse_date(request.query_params.get("end_date", ""))

    if start_date:
        trades = trades.filter(entry_time__date__gte=start_date)
    if end_date:
        trades = trades.filter(entry_time__date__lte=end_date)

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
            "average_holding_time": 0.0,
        })

    wins, losses, rr_ratios = [], [], []
    net_profit = 0
    equity_curve = []
    holding_durations = []

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

        # 🕒 Holding time
        if trade.entry_time and trade.exit_time:
            duration = trade.exit_time - trade.entry_time
            holding_durations.append(duration.total_seconds())

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

    avg_holding_time = round((sum(holding_durations) / len(holding_durations)) / 3600,
                             2) if holding_durations else 0  # in hours

    return Response({
        "total_trades": total_trades,
        "win_rate": win_rate,
        "avg_rr": avg_rr,
        "profit_factor": profit_factor,
        "net_profit": round(net_profit, 2),
        "average_profit": average_profit,
        "max_drawdown": round(max_dd, 2),
        "average_holding_time": float(round(avg_holding_time, 2)),
    })
