"""Added initial timestamp for Town

Revision ID: 0e7b49b2bc0c
Revises: e580aab87842
Create Date: 2024-04-02 02:13:43.243830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e7b49b2bc0c'
down_revision: Union[str, None] = 'e580aab87842'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
