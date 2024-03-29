"""New migration

Revision ID: e03ab4112073
Revises: 
Create Date: 2024-03-23 11:15:19.902389

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e03ab4112073'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('simultaneous_reports_generation', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('username'),
    schema='public'
    )
    op.create_table('generation_template',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('channel_list', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('from_date', sa.DateTime(), nullable=False),
    sa.Column('to_date', sa.DateTime(), nullable=False),
    sa.Column('report_type', sa.Enum('STATISTICAL', 'WORD_CLOUD', name='reporttypes'), nullable=False),
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('model_code', sa.String(), nullable=False),
    sa.Column('report_name', sa.String(), nullable=False),
    sa.Column('datasource_type', sa.String(), nullable=False),
    sa.Column('model_type', sa.Enum('SKLEARN', 'KERAS', 'BUILTIN', name='modeltypes'), nullable=False),
    sa.Column('classification_scope', sa.Enum('ENTIRE_POST', 'TOKENS', name='classificationscopes'), nullable=False),
    sa.Column('owner_username', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['owner_username'], ['public.user.username'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('report',
    sa.Column('report_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('report_type', sa.Enum('STATISTICAL', 'WORD_CLOUD', name='reporttypes'), nullable=False),
    sa.Column('processing_status', sa.Enum('POSTPONED', 'READY', 'PROCESSING', 'NEW', name='reportprocessingresult'), nullable=False),
    sa.Column('generation_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('report_failed_reason', sa.String(), nullable=True),
    sa.Column('report_warnings', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('report_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('owner_username', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['owner_username'], ['public.user.username'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('report_id'),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('report', schema='public')
    op.drop_table('generation_template', schema='public')
    op.drop_table('user', schema='public')
    # ### end Alembic commands ###
