"""initial migrate

Revision ID: 6671e5cac845
Revises: 73fac4f01ce4
Create Date: 2019-11-05 02:00:14.225778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6671e5cac845'
down_revision = '73fac4f01ce4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('cover', sa.LargeBinary(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('file', 'cover')
    # ### end Alembic commands ###