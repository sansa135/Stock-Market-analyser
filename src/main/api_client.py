import requests

BASE_URL = "https://www.alphavantage.co/query"


def fetch_daily_series(symbol, api_key):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key
    }

    response = requests.get(BASE_URL, params=params, timeout=15)
    response.raise_for_status()
    return response.json()