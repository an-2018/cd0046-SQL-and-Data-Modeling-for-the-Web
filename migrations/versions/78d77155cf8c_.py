"""empty message

Revision ID: 78d77155cf8c
Revises: 4dd41dc425d0
Create Date: 2022-08-14 11:02:50.481797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78d77155cf8c'
down_revision = '4dd41dc425d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('genres', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('genres', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('genres', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('genres', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
