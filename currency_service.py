import requests
from sqlalchemy.orm import Session

from models import Currency

token = 'feaf3e9f5c5939f46ed617cb3b1d76b3'
API_URL = f"http://api.coinlayer.com/live?access_key={token}"


class CurrencyService:
    def __init__(self, db: Session):
        self.db = db

    def fetch_exchange_rates(self):
        response = requests.get(API_URL)
        if response.status_code != 200:
            print(f"Error: API responded with status {response.status_code}")
            print(response.text)
            return {}
        else:
            return response.json().get("rates", {}) 

    def update_exchange_rates(self):
        exchange_rates = self.fetch_exchange_rates()
        for code, rate in exchange_rates.items():
            currency = self.db.query(Currency).filter(Currency.code == code).first()
            if currency:
                currency.rate = rate
            else:
                currency = Currency(code=code, rate=rate)
                self.db.add(currency)
        self.db.commit()

    def convert_currency(self, from_currency_code: str, to_currency_code: str, amount: float) -> float:
        from_currency = self.db.query(Currency).filter(Currency.code == from_currency_code).first()
        to_currency = self.db.query(Currency).filter(Currency.code == to_currency_code).first()

        if not from_currency or not to_currency:
            raise ValueError("Invalid currency code(s)")

        converted_amount = amount * (to_currency.rate / from_currency.rate)
        return converted_amount
