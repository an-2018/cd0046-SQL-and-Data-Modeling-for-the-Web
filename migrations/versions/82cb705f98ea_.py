"""empty message

Revision ID: 82cb705f98ea
Revises: 04251ca6a71d
Create Date: 2022-08-14 19:29:33.312602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82cb705f98ea'
down_revision = '04251ca6a71d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shows', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('name', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
