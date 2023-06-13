"""empty message

Revision ID: eb6f9660720a
Revises: 1bba2bc00272
Create Date: 2023-04-10 15:25:54.217251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb6f9660720a'
down_revision = '1bba2bc00272'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_color_module',
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('server', sa.Integer(), nullable=True),
    sa.Column('player', sa.Integer(), nullable=True),
    sa.Column('tag', sa.String(length=32), nullable=False),
    sa.Column('tag_color', sa.String(length=8), nullable=False),
    sa.Column('name_color', sa.String(length=8), nullable=False),
    sa.Column('text_color', sa.String(length=8), nullable=False),
    sa.ForeignKeyConstraint(['player'], ['players.id'], name='fk_chat_color_module_players_id_player'),
    sa.ForeignKeyConstraint(['server'], ['servers.id'], name='fk_chat_color_module_servers_id_server'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_color_module')
    # ### end Alembic commands ###