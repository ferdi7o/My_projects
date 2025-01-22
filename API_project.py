import requests


def convert_currencies(currency):
    api_key = '53b7bb339000b9554865a0a5'
    url = f"https://v6.exchangerate-api.com/v6/ {api_key}/latest/USD"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        conversion_rate = data['conversion_rates']['USD']
        dollars = currency * conversion_rate

        return f'{dollars:.3f}'

    else:
        return "Error fetching excange rate"

currency_value = int(input())
