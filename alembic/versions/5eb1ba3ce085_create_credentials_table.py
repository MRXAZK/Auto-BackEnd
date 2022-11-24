"""create credentials table

Revision ID: 5eb1ba3ce085
Revises: a249d791602b
Create Date: 2022-11-24 21:30:27.111102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5eb1ba3ce085'
down_revision = 'a249d791602b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'dt_credentials',
        sa.Column('id_credential', sa.Integer, primary_key=True),
        sa.Column('id_user', sa.Integer, nullable=False),
        sa.Column('profile_name', sa.String(255)),
        sa.Column('access_id', sa.String(255)),
        sa.Column('secret_access', sa.String(255)),
        sa.Column('date_created', sa.DateTime, server_default=sa.func.now()),
    )
    op.create_foreign_key('fk_user', 'dt_credentials', 'dt_user', ['id_user'], ['id_user'])
    


def downgrade():
    op.drop_table('dt_credentials')
