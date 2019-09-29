"""initial migration

Revision ID: d8cbcfb636e6
Revises: 43cc5d7bbbbf
Create Date: 2019-09-27 10:16:18.939151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8cbcfb636e6'
down_revision = '43cc5d7bbbbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('downloads', sa.Integer(), nullable=True))
    op.drop_column('file', '_downloads')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('_downloads', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('file', 'downloads')
    # ### end Alembic commands ###
