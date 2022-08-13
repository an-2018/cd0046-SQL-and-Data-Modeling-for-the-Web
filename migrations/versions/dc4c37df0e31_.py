"""empty message

Revision ID: dc4c37df0e31
Revises: c7835c2b3f9a
Create Date: 2022-08-12 23:56:38.086031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc4c37df0e31'
down_revision = 'c7835c2b3f9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'location_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'location_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###