"""empty message

Revision ID: 1460af0a4699
Revises: 
Create Date: 2021-04-04 23:49:01.778909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1460af0a4699'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=32), nullable=False),
    sa.Column('is_confirmed', sa.Boolean(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('location', sa.String(length=32), nullable=True),
    sa.Column('about_me', sa.Text(), nullable=True),
    sa.Column('league', sa.String(length=16), nullable=True),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.Column('highscore', sa.Integer(), nullable=True),
    sa.Column('last_ten_scores', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###