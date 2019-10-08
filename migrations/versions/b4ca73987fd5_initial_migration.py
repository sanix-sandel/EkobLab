"""initial migration

Revision ID: b4ca73987fd5
Revises: a7c204234b4b
Create Date: 2019-10-06 18:11:42.453822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4ca73987fd5'
down_revision = 'a7c204234b4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'genre',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'genre',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    # ### end Alembic commands ###