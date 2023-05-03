from dependency_injector import containers, providers
from sqlalchemy.orm import Session

from database import SessionLocal
from currency_service import CurrencyService 


class ApplicationContainer(containers.DeclarativeContainer):
    session_factory = providers.Factory(SessionLocal)
    currency_service_factory = providers.Factory(CurrencyService)
