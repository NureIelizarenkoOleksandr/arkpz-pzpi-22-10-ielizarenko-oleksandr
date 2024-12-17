"""lb 1 procedure function

Revision ID: 09c59111bc9a
Revises: 2538edfcbb60
Create Date: 2024-12-16 22:15:28.935162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09c59111bc9a'
down_revision: Union[str, None] = '2538edfcbb60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION GetTopSoldGoodsByWorkerName(WorkerName VARCHAR)
RETURNS TABLE(Good_Name VARCHAR) AS
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM workers WHERE name = WorkerName) THEN
        RETURN QUERY SELECT 'Відсутні продажі'::VARCHAR;
        RETURN;
    END IF;

    RETURN QUERY
    SELECT g.name
    FROM workers w
    JOIN departments d ON w.dept_id = d.dept_id
    JOIN goods g ON d.dept_id = g.dept_id
    JOIN sales s ON g.good_id = s.good_id
    WHERE w.name = WorkerName
    GROUP BY g.name
    HAVING SUM(s.quantity) = 
        (
            SELECT MAX(TotalQuantity)
            FROM 
            (
                SELECT SUM(s2.quantity) AS TotalQuantity
                FROM workers w2
                JOIN departments d2 ON w2.dept_id = d2.dept_id
                JOIN goods g2 ON d2.dept_id = g2.dept_id
                JOIN sales s2 ON g2.good_id = s2.good_id
                WHERE w2.name = WorkerName
                GROUP BY g2.name
            ) AS SubQuery
        );
    IF NOT EXISTS (SELECT 1 FROM workers w
                   JOIN departments d ON w.dept_id = d.dept_id
                   JOIN goods g ON d.dept_id = g.dept_id
                   JOIN sales s ON g.good_id = s.good_id
                   WHERE w.name = WorkerName) THEN
        RETURN QUERY SELECT 'Відсутні продажі'::VARCHAR;
    END IF;
    
END;
$$ LANGUAGE plpgsql;
    """)

op.execute("""
CREATE OR REPLACE PROCEDURE UpdateGoodsDescriptionWithDiscount(GoodName VARCHAR, Discount INT)
LANGUAGE plpgsql
AS
$$
BEGIN
    IF EXISTS (SELECT 1 FROM goods WHERE name = GoodName) THEN
        UPDATE goods
        SET description = description || ' Знижка ' || Discount || ' %'
        WHERE name = GoodName;

        RAISE NOTICE 'Опис товару успішно оновлено.';
    ELSE
        RAISE NOTICE 'Товар з таким ім''ям не знайдено.';
    END IF;
END;
$$;

""")


def downgrade() -> None:
    op.execute("""
DROP FUNCTION IF EXISTS GetTopSoldGoodsByWorkerName(VARCHAR);
DROP PROCEDURE IF EXISTS UpdateGoodsDescriptionWithDiscount(VARCHAR, INT);

    """)
