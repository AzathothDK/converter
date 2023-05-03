from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import asyncio
from typing import List

from models import Currency
from schemas import CurrencyResponse, ConversionRequest
from containers import ApplicationContainer

router = APIRouter()

container = ApplicationContainer()

def get_db():
    db = container.session_factory()
    try:
        yield db
    finally:
        db.close()

@router.on_event("startup")
async def startup_event():
    asyncio.create_task(update_currencies_task())

async def update_currencies_task():
    while True:
        db = container.session_factory()
        currency_service = container.currency_service_factory(db=db)
        currency_service.update_exchange_rates()
        await asyncio.sleep(300)
        
@router.get("/exchange-rates", response_model=List[CurrencyResponse])
def get_exchange_rates(db: Session = Depends(get_db)):
    currencies = db.query(Currency).all()
    return [CurrencyResponse(**currency.to_dict()) for currency in currencies]

@router.post("/convert")
def convert(conversion_request: ConversionRequest, db: Session = Depends(get_db)):
    currency_service = container.currency_service_factory(db)
    try:
        result = currency_service.convert_currency(
            conversion_request.from_currency,
            conversion_request.to_currency,
            conversion_request.amount
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "from_currency": conversion_request.from_currency,
        "to_currency": conversion_request.to_currency,
        "amount": conversion_request.amount,
        "result": result
    }


