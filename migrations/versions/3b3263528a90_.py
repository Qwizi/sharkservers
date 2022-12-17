"""empty message

Revision ID: 3b3263528a90
Revises: 5d744818e557
Create Date: 2022-12-17 02:20:38.753463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b3263528a90'
down_revision = '5d744818e557'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('steamprofiles', sa.Column('username', sa.String(length=32), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('steamprofiles', 'username')
    # ### end Alembic commands ###