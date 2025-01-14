"""empty message

Revision ID: 5598d640a390
Revises: dc4c37df0e31
Create Date: 2022-08-13 00:04:26.401631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5598d640a390'
down_revision = 'dc4c37df0e31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('artists_location_id_fkey', 'artists', type_='foreignkey')
    op.drop_column('artists', 'location_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('location_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('artists_location_id_fkey', 'artists', 'locations', ['location_id'], ['id'])
    # ### end Alembic commands ###
