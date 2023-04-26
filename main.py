from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from models import Currency, Base
from schemas import CurrencyResponse, ConversionRequest
from containers import ApplicationContainer
from database import engine

app = FastAPI()
container = ApplicationContainer()

Base.metadata.create_all(bind=engine)


def get_db():
    db = container.session_factory()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    currency_service = container.currency_service_factory()
    currency_service.update_exchange_rates()


@app.get("/exchange-rates", response_model=List[CurrencyResponse])
def get_exchange_rates(db: Session = Depends(get_db)):
    currencies = db.query(Currency).all()
    return [CurrencyResponse(**currency.to_dict()) for currency in currencies]


@app.post("/convert")
def convert(conversion_request: ConversionRequest, db: Session = Depends(get_db)):
    currency_service = container.currency_service_factory(db=db)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
