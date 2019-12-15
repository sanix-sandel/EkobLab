"""initial migrate

Revision ID: 734b2741b535
Revises: a9ab4add415b
Create Date: 2019-11-24 19:01:56.981012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '734b2741b535'
down_revision = 'a9ab4add415b'
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