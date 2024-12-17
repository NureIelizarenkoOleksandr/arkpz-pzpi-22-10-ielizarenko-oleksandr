from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator, Field

from schemas.sales import SalesOut


class GoodOut(BaseModel):
    good_id: UUID
    name: str
    price: int
    quantity: int
    producer: str
    description: str

    @field_validator("good_id", mode="before")
    def convert_good_id_to_str(cls, value):
        return str(value)

    class Config:
        orm_mode = True

class GoodSaleSchema(GoodOut):
    sales: List[SalesOut]


class GoodCreate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    producer: Optional[str] = None
    description: Optional[str] = None