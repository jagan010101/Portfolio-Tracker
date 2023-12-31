"""empty message

Revision ID: 5ed3ac9a5f12
Revises: 1a2882e4faf3
Create Date: 2023-06-16 21:40:29.743245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ed3ac9a5f12'
down_revision = '1a2882e4faf3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('yesterday', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('yesterday', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###
