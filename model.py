from collections import defaultdict
import datetime

def predict_next_month(expenses):
    """
    Predict next month's total expense using a simple linear regression
    built from scratch (no sklearn dependency issues on fresh installs).
    Falls back gracefully if there's not enough data.
    """
    if not expenses:
        return {"predicted": 0, "message": "No expense data available to predict."}

    # Aggregate expenses by month index
    monthly = defaultdict(float)
    for e in expenses:
        try:
            date = datetime.date.fromisoformat(e["date"])
            key = date.year * 12 + date.month  # monotonic month index
            monthly[key] += e["amount"]
        except Exception:
            continue

    if len(monthly) < 2:
        total = sum(monthly.values())
        return {
            "predicted": round(total, 2),
            "message": "Not enough monthly data for regression. Showing current total.",
            "months_used": len(monthly)
        }

    keys = sorted(monthly.keys())
    # Normalize x so regression is numerically stable
    x_raw = list(range(len(keys)))
    y = [monthly[k] for k in keys]

    n = len(x_raw)
    x_mean = sum(x_raw) / n
    y_mean = sum(y) / n

    numerator = sum((x_raw[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    denominator = sum((x_raw[i] - x_mean) ** 2 for i in range(n))

    if denominator == 0:
        slope = 0
    else:
        slope = numerator / denominator

    intercept = y_mean - slope * x_mean
    next_x = len(keys)  # one step beyond last known month
    predicted = intercept + slope * next_x

    trend = "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"

    return {
        "predicted": round(max(predicted, 0), 2),
        "trend": trend,
        "slope": round(slope, 2),
        "months_used": n,
        "message": f"Based on {n} months of data. Spending trend is {trend}."
    }
