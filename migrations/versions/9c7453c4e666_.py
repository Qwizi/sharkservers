"""empty message

Revision ID: 9c7453c4e666
Revises: 1cde8614c458
Create Date: 2023-02-09 01:36:21.623252

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "9c7453c4e666"
down_revision = "1cde8614c458"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "players", ["profile_url"])
    op.create_unique_constraint(None, "steamrep_profiles", ["profile_url"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "steamrep_profiles", type_="unique")
    op.drop_constraint(None, "players", type_="unique")
    # ### end Alembic commands ###