"""empty message

Revision ID: f15f582db272
Revises: c72d3c31b00d
Create Date: 2023-12-04 11:59:36.277714

"""
from alembic import op
import sqlalchemy as sa
import ormar
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f15f582db272"
down_revision = "c72d3c31b00d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("sourcemod_apis")
    op.add_column(
        "servers", sa.Column("api_url", sa.String(length=256), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("servers", "api_url")
    op.create_table(
        "sourcemod_apis",
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("tag", sa.VARCHAR(length=64), autoincrement=False, nullable=False),
        sa.Column("url", sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="sourcemod_apis_pkey"),
        sa.UniqueConstraint("tag", name="sourcemod_apis_tag_key"),
    )
    # ### end Alembic commands ###
