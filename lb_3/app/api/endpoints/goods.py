from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from models.company import Good
from schemas.goods import GoodOut, GoodSaleSchema, GoodCreate

router = APIRouter()


@router.get("", response_model=List[GoodOut])
def get_all_goods(
    db = Depends(get_db)
):
    goods = db.query(Good).all()
    return goods


@router.get("/top-sold")
def get_top_sold_goods(name: str, db: Session = Depends(get_db)):
    """
    Call GetTopSoldGoodsByWorkerName.
    """
    try:
        result = db.execute(
            text("SELECT * FROM GetTopSoldGoodsByWorkerName(:worker_name)"),
            {"worker_name": name}
        ).fetchall()

        if not result or result[0][0] == 'Відсутні продажі':
            raise HTTPException(status_code=404, detail=f"Відсутні продажі для працівника {name}")
        goods = [row[0] for row in result]
        return goods

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update-description")
def update_goods_description(good_name: str, discount: int, db: Session = Depends(get_db)):
    try:
        good = db.query(Good).filter(Good.name == good_name).first()

        if not good:
            raise HTTPException(status_code=404, detail=f"Товар {good_name} не знайдено")

        db.execute(
            text("""
                    CALL UpdateGoodsDescriptionWithDiscount(:good_name, :discount)
                """),
            {"good_name": good_name, "discount": discount}
        )
        db.commit()

        return {"message": "Товар успішно оновлено"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{good_id}", response_model=GoodSaleSchema)
def get_good_by_id(good_id: UUID, db: Session = Depends(get_db)):
    good = db.query(Good).options(joinedload(Good.sales)).filter(Good.good_id == good_id).first()
    if not good:
        raise HTTPException(status_code=404, detail="Good not found")
    return good


@router.post("", response_model=GoodOut)
def create_good(good: GoodCreate, db: Session = Depends(get_db)):
    new_good = Good(**good.model_dump())
    db.add(new_good)
    db.commit()
    db.refresh(new_good)
    return new_good


@router.put("/{good_id}", response_model=GoodOut)
def update_good(good_id: UUID, good: GoodCreate, db: Session = Depends(get_db)):
    db_good = db.query(Good).filter(Good.good_id == good_id).first()
    if not db_good:
        raise HTTPException(status_code=404, detail="Good not found")
    for key, value in good.model_dump(exclude_unset=True).items():
        setattr(db_good, key, value)
    db.commit()
    db.refresh(db_good)
    return db_good



@router.get("/test-endpoint")
def test_endpoint():
    return {"hello": "world"}