from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SalesOut(BaseModel):
    sale_id: UUID
    check_no: int
    good_id: UUID
    date_sale: Optional[datetime]
    quantity: int

    class Config:
        orm_mode = True

class GoodOut(BaseModel):
    good_id: UUID
    name: str
    quantity: int

    class Config:
        orm_mode = True

class SaleGood(BaseModel):
    sale_id: UUID
    check_no: int
    date_sale: datetime
    quantity: int
    good: Optional[GoodOut]

    class Config:
        orm_mode = True

class SaleCreate(BaseModel):
    check_no: Optional[int]
    quantity: Optional[int]
    good_id: UUID

