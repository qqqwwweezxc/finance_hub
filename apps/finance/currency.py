from decimal import Decimal, ROUND_HALF_UP

import requests


def get_exchange_rate(from_currency, to_currency):
    if from_currency == to_currency:
        return Decimal("1")

    url = f"https://open.er-api.com/v6/latest/{from_currency}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    if data.get("result") != "success":
        raise ValueError("Currency API returned an unsuccessful response.")

    rates = data.get("rates", {})

    if to_currency not in rates:
        raise ValueError(f"Currency {to_currency} is not supported by exchange API.")

    return Decimal(str(rates[to_currency]))


def convert_money(amount, rate):
    return (amount * rate).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )