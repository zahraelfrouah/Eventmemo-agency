"""added place

Revision ID: d522d05401c2
Revises: cd5d6b5f0ff2
Create Date: 2023-06-09 18:23:57.391473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd522d05401c2'
down_revision = 'cd5d6b5f0ff2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('place', sa.String(length=90), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('place')

    # ### end Alembic commands ###
