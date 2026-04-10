def extract_stock_points(json_data):
    time_series = json_data.get("Time Series (Daily)", {})
    points = []

    for date, values in time_series.items():
        point = {
            "date": date,
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"]),
            "volume": int(values["5. volume"])
        }
        points.append(point)

    points.sort(key=lambda x: x["date"], reverse=True)
    return points


def latest_point(points):
    return points[0] if points else None


def highest_close(points):
    return max(p["close"] for p in points) if points else 0


def lowest_close(points):
    return min(p["close"] for p in points) if points else 0


def moving_average(points, days=7):
    if not points:
        return 0

    selected = points[:days]
    return sum(p["close"] for p in selected) / len(selected)