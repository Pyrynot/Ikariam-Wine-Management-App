"""Remove unique constraint from town_name

Revision ID: 8ed053ca5f24
Revises: 
Create Date: 2024-04-01 17:37:24.076604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ed053ca5f24'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_towns_town_name', table_name='towns')
    op.create_index(op.f('ix_towns_town_name'), 'towns', ['town_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_towns_town_name'), table_name='towns')
    op.create_index('ix_towns_town_name', 'towns', ['town_name'], unique=1)
    # ### end Alembic commands ###
