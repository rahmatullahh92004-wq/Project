#!/usr/bin/env python3
import requests
import time
from rich.console import Console
from rich.table import Table

API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 20,
    "page": 1,
    "price_change_percentage": "1h,24h,7d"
}

console = Console()

def fetch_crypto_data():
    try:
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching data:[/red] {e}")
        return []

def display_data(coins):
    table = Table(title="Top 20 Cryptocurrencies")
    table.add_column("Rank", justify="right")
    table.add_column("Name")
    table.add_column("Symbol")
    table.add_column("Price (USD)", justify="right")
    table.add_column("1h %", justify="right")
    table.add_column("24h %", justify="right")
    table.add_column("7d %", justify="right")

    for coin in coins:
        table.add_row(
            str(coin.get("market_cap_rank", "")),
            coin.get("name", ""),
            coin.get("symbol", "").upper(),
            f"${coin.get('current_price', 0):,.2f}",
            f"{coin.get('price_change_percentage_1h_in_currency', 0):.2f}%",
            f"{coin.get('price_change_percentage_24h_in_currency', 0):.2f}%",
            f"{coin.get('price_change_percentage_7d_in_currency', 0):.2f}%"
        )

    console.clear()
    console.print(table)

def main():
    while True:
        coins = fetch_crypto_data()
        if coins:
            display_data(coins)
        console.print("[green]Next update in 1 minute...[/green]")
        time.sleep(60)  # refresh every 1 minute

if __name__ == "__main__":
    main()
