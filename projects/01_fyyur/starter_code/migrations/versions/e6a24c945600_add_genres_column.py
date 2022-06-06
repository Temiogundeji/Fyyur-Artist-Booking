"""Add genres column

Revision ID: e6a24c945600
Revises: a2c9e24d4b55
Create Date: 2022-06-06 05:12:06.476081

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e6a24c945600'
down_revision = 'a2c9e24d4b55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', 'created',
    existing_type=postgresql.TIMESTAMP(),
    nullable=True)
    op.execute('UPDATE "Artist" SET created = CURRENT_TIMESTAMP WHERE created IS NULL;')
    op.alter_column('Artist', 'created', nullable=False)
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'genres')
    op.alter_column('Artist', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###
