from dependency_injector import containers, providers
from sqlalchemy.orm import Session

from database import SessionLocal
from currency_service import update_exchange_rates, convert_currency


class CurrencyService:
    def __init__(self, db: Session):
        self.db = db

    def update_exchange_rates(self):
        return update_exchange_rates(self.db)

    def convert_currency(self, from_currency: str, to_currency: str, amount: float) -> float:
        return convert_currency(self.db, from_currency, to_currency, amount)


class ApplicationContainer(containers.DeclarativeContainer):
    session_factory = providers.Factory(SessionLocal)
    currency_service_factory = providers.Factory(CurrencyService, db=session_factory)
