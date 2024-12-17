"""lb 2 trigger

Revision ID: c62c6e6b14e1
Revises: 09c59111bc9a
Create Date: 2024-12-17 20:56:47.034101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c62c6e6b14e1'
down_revision: Union[str, None] = '09c59111bc9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'Sales'
trigger_name = 'trg_PreventExcessiveSales'


def upgrade():
    # Создание функции триггера
    op.execute("""
    CREATE OR REPLACE FUNCTION prevent_excessive_sales()
    RETURNS TRIGGER AS $$
    DECLARE
        total_quantity INT;
        affected_good_id UUID;  -- Используем UUID для идентификатора товара
    BEGIN
        -- Получаем Good_id для вставленных или обновленных товаров
        IF TG_OP = 'INSERT' THEN
            affected_good_id := NEW.Good_id;
        ELSIF TG_OP = 'UPDATE' THEN
            affected_good_id := NEW.Good_id;
        END IF;

        -- Рассчитываем общее количество продаж для товара
        SELECT COALESCE(SUM(Quantity), 0) INTO total_quantity
        FROM Sales
        WHERE Good_id = affected_good_id;

        -- Проверка превышения лимита
        IF total_quantity + NEW.Quantity > 100 THEN
            RAISE EXCEPTION 'Операція неможлива: кількість продажів товару перевищує 100 для товару %', affected_good_id;
        END IF;

        -- Возвращаем NEW для INSERT/UPDATE
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Создание триггера
    op.execute("""
    CREATE TRIGGER trg_PreventExcessiveSales
    BEFORE INSERT OR UPDATE ON Sales
    FOR EACH ROW  -- Для каждой строки
    EXECUTE FUNCTION prevent_excessive_sales();
    """)


def downgrade():
    # Удаление триггера
    op.execute("DROP TRIGGER IF EXISTS trg_PreventExcessiveSales ON Sales;")

    # Удаление функции
    op.execute("DROP FUNCTION IF EXISTS prevent_excessive_sales();")
