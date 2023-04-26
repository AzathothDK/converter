import requests
from sqlalchemy.orm import Session
from typing import Tuple

from models import Currency

token = 'your_token'
API_URL = f"http://api.coinlayer.com/live?access_key={token}"

def fetch_exchange_rates():
    response = requests.get(API_URL)
    return response.json()["rates"]

def update_exchange_rates(db: Session):
    exchange_rates = fetch_exchange_rates()
    for code, rate in exchange_rates.items():
        currency = db.query(Currency).filter(Currency.code == code).first()
        if currency:
            currency.rate = rate
        else:
            currency = Currency(code=code, rate=rate)
            db.add(currency)
    db.commit()


def convert_currency(db: Session, from_currency_code: str, to_currency_code: str, amount: float) -> float:
    from_currency = db.query(Currency).filter(Currency.code == from_currency_code).first()
    to_currency = db.query(Currency).filter(Currency.code == to_currency_code).first()

    if not from_currency or not to_currency:
        raise ValueError("Invalid currency code(s)")

    converted_amount = amount * (to_currency.rate / from_currency.rate)
    return converted_amount
