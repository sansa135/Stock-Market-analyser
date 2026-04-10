from api_client import fetch_daily_series
from analytics import (
    extract_stock_points,
    latest_point,
    highest_close,
    lowest_close,
    moving_average,
)
import tkinter as tk

API_KEY = "3JT84K8VX0AD8BYH"


def get_trend(points):
    if len(points) < 7:
        return "Not enough data"

    recent_avg = sum(p["close"] for p in points[:7]) / 7
    older_avg = sum(p["close"] for p in points[7:14]) / 7 if len(points) >= 14 else recent_avg

    if recent_avg > older_avg:
        return "Uptrend"
    elif recent_avg < older_avg:
        return "Downtrend"
    return "Sideways"


# ================= SINGLE STOCK GRAPH =================
def plot_graph(points, symbol):
    data = points[:30]
    data.reverse()

    closes = [p["close"] for p in data]
    dates = [p["date"][5:] for p in data]

    width = 900
    height = 500
    margin = 60

    root = tk.Tk()
    root.title(f"{symbol} Graph")
    root.geometry(f"{width}x{height}")

    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

    canvas.create_text(width // 2, 20, text=f"{symbol} - Last 30 Days", font=("Arial", 16, "bold"))

    min_val = min(closes)
    max_val = max(closes)

    if max_val == min_val:
        max_val += 1

    # axes
    canvas.create_line(margin, height - margin, width - margin, height - margin, width=2)
    canvas.create_line(margin, margin, margin, height - margin, width=2)

    # Y-axis labels
    for i in range(6):
        y = margin + i * (height - 2 * margin) / 5
        value = max_val - i * (max_val - min_val) / 5
        canvas.create_text(margin - 30, y, text=f"{value:.1f}")

    coords = []

    for i, close in enumerate(closes):
        x = margin + i * (width - 2 * margin) / (len(closes) - 1)
        y = height - margin - ((close - min_val) / (max_val - min_val)) * (height - 2 * margin)
        coords.append((x, y))

    # draw line
    for i in range(len(coords) - 1):
        canvas.create_line(coords[i][0], coords[i][1],
                           coords[i + 1][0], coords[i + 1][1],
                           fill="#0077cc", width=3)

    # draw points
    for i, (x, y) in enumerate(coords):
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")
        if i % 5 == 0:
            canvas.create_text(x, height - margin + 15, text=dates[i], angle=45)

    # last value label
    x_last, y_last = coords[-1]
    canvas.create_text(x_last + 40, y_last,
                       text=f"{closes[-1]:.2f}",
                       fill="green",
                       font=("Arial", 10, "bold"))

    root.mainloop()


# ================= COMPARISON GRAPH =================
def plot_comparison(points1, points2, symbol1, symbol2):
    data1 = points1[:30]
    data2 = points2[:30]

    data1.reverse()
    data2.reverse()

    closes1 = [p["close"] for p in data1]
    closes2 = [p["close"] for p in data2]
    dates = [p["date"][5:] for p in data1]

    width = 1000
    height = 600
    margin = 70

    root = tk.Tk()
    root.title(f"{symbol1} vs {symbol2}")
    root.geometry(f"{width}x{height}")

    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

    canvas.create_text(width // 2, 25, text=f"{symbol1} vs {symbol2}", font=("Arial", 18, "bold"))

    all_values = closes1 + closes2
    min_val = min(all_values)
    max_val = max(all_values)

    if max_val == min_val:
        max_val += 1

    # axes
    canvas.create_line(margin, height - margin, width - margin, height - margin, width=2)
    canvas.create_line(margin, margin, margin, height - margin, width=2)

    # Y-axis labels
    for i in range(6):
        y = margin + i * (height - 2 * margin) / 5
        value = max_val - i * (max_val - min_val) / 5
        canvas.create_text(margin - 35, y, text=f"{value:.1f}")

    coords1 = []
    coords2 = []

    for i in range(len(closes1)):
        x = margin + i * (width - 2 * margin) / (len(closes1) - 1)

        y1 = height - margin - ((closes1[i] - min_val) / (max_val - min_val)) * (height - 2 * margin)
        y2 = height - margin - ((closes2[i] - min_val) / (max_val - min_val)) * (height - 2 * margin)

        coords1.append((x, y1))
        coords2.append((x, y2))

    # draw lines
    for i in range(len(coords1) - 1):
        canvas.create_line(coords1[i][0], coords1[i][1],
                           coords1[i + 1][0], coords1[i + 1][1],
                           fill="blue", width=3)

    for i in range(len(coords2) - 1):
        canvas.create_line(coords2[i][0], coords2[i][1],
                           coords2[i + 1][0], coords2[i + 1][1],
                           fill="red", width=3)

    # draw points
    for x, y in coords1:
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")

    for x, y in coords2:
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")

    # x-axis labels
    for i, (x, y) in enumerate(coords1):
        if i % 5 == 0:
            canvas.create_text(x, height - margin + 18, text=dates[i], angle=45)

    # legend
    canvas.create_text(120, 50, text=symbol1, fill="blue", font=("Arial", 12, "bold"))
    canvas.create_text(220, 50, text=symbol2, fill="red", font=("Arial", 12, "bold"))

    # last values
    x1, y1 = coords1[-1]
    x2, y2 = coords2[-1]

    canvas.create_text(x1 + 35, y1, text=f"{closes1[-1]:.2f}", fill="blue")
    canvas.create_text(x2 + 35, y2, text=f"{closes2[-1]:.2f}", fill="red")

    root.mainloop()


# ================= MAIN =================
def main():
    choice = input("1 = Single Graph, 2 = Compare: ")

    if choice == "1":
        symbol = input("Enter stock: ").upper()

        data = fetch_daily_series(symbol, API_KEY)
        points = extract_stock_points(data)

        plot_graph(points, symbol)

    elif choice == "2":
        s1 = input("Stock 1: ").upper()
        s2 = input("Stock 2: ").upper()

        p1 = extract_stock_points(fetch_daily_series(s1, API_KEY))
        p2 = extract_stock_points(fetch_daily_series(s2, API_KEY))

        plot_comparison(p1, p2, s1, s2)

    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()