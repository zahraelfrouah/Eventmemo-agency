"""Add content column to posts table

Revision ID: 917ecc00d452
Revises: 504604ad802f
Create Date: 2023-06-03 00:18:06.937290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '917ecc00d452'
down_revision = '504604ad802f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content', sa.Text(length=90), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('content')

    # ### end Alembic commands ###
