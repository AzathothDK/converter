from pydantic import BaseModel
from typing import Optional


class CurrencyResponse(BaseModel):
    id: int
    code: str
    rate: float


class ConversionRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
