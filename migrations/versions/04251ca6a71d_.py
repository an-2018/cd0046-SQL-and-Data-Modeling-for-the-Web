"""empty message

Revision ID: 04251ca6a71d
Revises: 42058533a630
Create Date: 2022-08-14 18:46:07.759531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04251ca6a71d'
down_revision = '42058533a630'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.drop_column('artists', 'seeking_talent')
    op.alter_column('venues', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.add_column('artists', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('artists', 'seeking_venue')
    # ### end Alembic commands ###
