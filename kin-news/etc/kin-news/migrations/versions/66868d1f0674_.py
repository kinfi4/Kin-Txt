"""empty message

Revision ID: 66868d1f0674
Revises: 
Create Date: 2023-06-01 18:59:23.536209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66868d1f0674'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kin_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('is_fetching', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_foreign_key(None, 'channel_rating', 'kin_user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'user_channel', 'kin_user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_channel', type_='foreignkey')
    op.drop_constraint(None, 'channel_rating', type_='foreignkey')
    op.drop_table('kin_user')
    # ### end Alembic commands ###
