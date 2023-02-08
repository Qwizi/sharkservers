"""empty message

Revision ID: bc0effee5db2
Revises: 92722ee88cc5
Create Date: 2023-02-08 23:17:41.595281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc0effee5db2'
down_revision = '92722ee88cc5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('steamrep_profiles', sa.Column('is_scammer', sa.Boolean(), nullable=True))
    op.drop_column('steamrep_profiles', 'scammer')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('steamrep_profiles', sa.Column('scammer', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('steamrep_profiles', 'is_scammer')
    # ### end Alembic commands ###
