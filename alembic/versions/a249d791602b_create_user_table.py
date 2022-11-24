"""create user table

Revision ID: a249d791602b
Revises: 
Create Date: 2022-11-22 21:16:57.851779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a249d791602b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'dt_user',
        sa.Column('id_user', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255)),
        sa.Column('email', sa.String(255)),
        sa.Column('hashed_password', sa.String(255)),
        sa.Column('disabled', sa.String(255))
    )



def downgrade():
    op.drop_table('dt_user')
