"""initial migrate

Revision ID: aff060bb950b
Revises: 54e2fe5249f2
Create Date: 2019-11-24 19:26:30.139896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aff060bb950b'
down_revision = '54e2fe5249f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'reads')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('reads', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###