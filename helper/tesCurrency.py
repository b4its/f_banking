import requests
from datetime import datetime
from typeCurrency import currencyType
class CurrencyConverter:
    def __init__(self):
        self.currency_types = dict(currencyType)
        self.api_url = "https://api.exchangerate-api.com/v4/latest/"

    def get_exchange_rate(self, from_currency, to_currency):
        try:
            response = requests.get(f"{self.api_url}{from_currency}")
            data = response.json()
            return data.get("rates", {}).get(to_currency)
        except Exception as e:
            print(f"Error mengambil data: {e}")
            return None

    def convert_currency(self, amount, from_currency, to_currency):
        if from_currency == to_currency:
            return amount
        rate = self.get_exchange_rate(from_currency, to_currency)
        if rate is None:
            return None
        return amount * rate

# Fungsi utilitas agar bisa dipanggil dari file luar
def convert_currency(amount, from_currency, to_currency):
    converter = CurrencyConverter()
    return converter.convert_currency(amount, from_currency, to_currency)
