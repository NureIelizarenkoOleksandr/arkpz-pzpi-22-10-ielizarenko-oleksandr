"""calculate delay

Revision ID: b89e8e9448c9
Revises: 3328f3d8ef0e
Create Date: 2025-01-12 20:31:59.630619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b89e8e9448c9'
down_revision: Union[str, None] = '3328f3d8ef0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedules', sa.Column('actual_arrival_time', sa.Time(), nullable=True))
    op.add_column('schedules', sa.Column('delay_minutes', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('schedules', 'delay_minutes')
    op.drop_column('schedules', 'actual_arrival_time')
    # ### end Alembic commands ###
