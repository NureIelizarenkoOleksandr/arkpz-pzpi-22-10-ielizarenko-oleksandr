from datetime import date

from sqlalchemy import Column, Integer, String, ForeignKey, Date, text, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


# Таблица WORKERS
class Worker(Base):
    __tablename__ = "workers"

    worker_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column("name", String)
    address = Column("address", String)
    dept_id = Column("dept_id", UUID, ForeignKey("departments.dept_id", ondelete="CASCADE"))
    information = Column("information", String)

    # Отношение к таблице DEPARTMENTS
    department = relationship("Department", back_populates="workers", passive_deletes=True)


# Таблица DEPARTMENTS
class Department(Base):
    __tablename__ = "departments"

    dept_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column("name", String)
    info = Column("info", String)

    # Отношение к WORKERS и GOODS
    workers = relationship("Worker", back_populates="department", passive_deletes=True)
    goods = relationship("Good", back_populates="department", passive_deletes=True)


# Таблица GOODS
class Good(Base):
    __tablename__ = "goods"

    good_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column("name", String)
    price = Column("price", Integer)
    quantity = Column("quantity", Integer)
    producer = Column("producer", String)
    dept_id = Column("dept_id", UUID, ForeignKey("departments.dept_id", ondelete="CASCADE"))
    description = Column("description", String)

    department = relationship("Department", back_populates="goods", passive_deletes=True)
    sales = relationship("Sale", back_populates="good", passive_deletes=True)


class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    check_no = Column("check_no", Integer)
    good_id = Column("good_id", UUID, ForeignKey("goods.good_id", ondelete="CASCADE"), nullable=False)
    date_sale = Column(Date, server_default=func.current_date())
    quantity = Column("quantity", Integer)
    good = relationship("Good", back_populates="sales", passive_deletes=True)
