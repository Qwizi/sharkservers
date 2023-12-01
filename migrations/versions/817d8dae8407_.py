"""empty message

Revision ID: 817d8dae8407
Revises: 6a35b24e57d4
Create Date: 2023-12-01 14:27:23.126505

"""
from alembic import op
import sqlalchemy as sa
import ormar


# revision identifiers, used by Alembic.
revision = "817d8dae8407"
down_revision = "6a35b24e57d4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "chat_color_module",
        "tag",
        existing_type=sa.VARCHAR(length=32),
        type_=sa.String(length=64),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "chat_color_module",
        "tag",
        existing_type=sa.String(length=64),
        type_=sa.VARCHAR(length=32),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
