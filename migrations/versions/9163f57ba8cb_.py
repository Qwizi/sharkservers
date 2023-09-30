"""empty message

Revision ID: 9163f57ba8cb
Revises: 3b1c47bdee0b
Create Date: 2023-09-16 20:53:27.442536

"""
from alembic import op
import sqlalchemy as sa
import ormar


# revision identifiers, used by Alembic.
revision = '9163f57ba8cb'
down_revision = '3b1c47bdee0b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('forum_threads', sa.Column('server', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_forum_threads_servers_id_server', 'forum_threads', 'servers', ['server'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_forum_threads_servers_id_server', 'forum_threads', type_='foreignkey')
    op.drop_column('forum_threads', 'server')
    # ### end Alembic commands ###