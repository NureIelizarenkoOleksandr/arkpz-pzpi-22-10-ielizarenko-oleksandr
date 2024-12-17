from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from psycopg2.errors import RaiseException
from starlette import status

from app.db.session import get_db
from models.company import Sale
from schemas.sales import SalesOut, SaleGood, SaleCreate

router = APIRouter()

@router.get("", response_model=List[SalesOut])
def get_sales(db=Depends(get_db)):
    sales = db.query(Sale).all()
    return sales


@router.get("/{sale_id}", response_model=SaleGood)
def get_good_by_id(sale_id: UUID, db: Session = Depends(get_db)):
    good = db.query(Sale).options(joinedload(Sale.good)).filter(Sale.sale_id == sale_id).first()
    if not good:
        raise HTTPException(status_code=404, detail="Good not found")
    return good


@router.post("", response_model=SalesOut)
def create_good(sale: SaleCreate, db: Session = Depends(get_db)):
    try:
        new_good = Sale(**sale.model_dump())
        db.add(new_good)
        db.commit()
        db.refresh(new_good)
        return new_good
    except SQLAlchemyError as e:
        db.rollback()
        if isinstance(e.__cause__, RaiseException):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Операція неможлива: кількість продажів товару перевищує 100."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера."
            )


@router.put("/{sale_id}", response_model=SalesOut)
def update_good(sale_id: UUID, sale: SaleCreate, db: Session = Depends(get_db)):
    try:
        db_good = db.query(Sale).filter(Sale.sale_id == sale_id).first()
        if not db_good:
            raise HTTPException(status_code=404, detail="Good not found")
        for key, value in sale.model_dump(exclude_unset=True).items():
            setattr(db_good, key, value)
        db.commit()
        db.refresh(db_good)
        return db_good

    except SQLAlchemyError as e:
        db.rollback()
        if isinstance(e.__cause__, RaiseException):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Операція неможлива: кількість продажів товару перевищує 100."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера."
            )