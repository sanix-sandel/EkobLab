"""initial migration

Revision ID: dec80f6bd043
Revises: 1846dd90fac3
Create Date: 2019-09-27 17:40:14.809554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dec80f6bd043'
down_revision = '1846dd90fac3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('downloaded', sa.Integer(), nullable=True))
    op.drop_column('file', '_downloads')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('_downloads', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('file', 'downloaded')
    # ### end Alembic commands ###