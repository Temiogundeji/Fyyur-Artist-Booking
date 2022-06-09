"""recreate show model

Revision ID: b8dd4670bd05
Revises: a7db9b22c525
Create Date: 2022-06-09 14:38:03.115019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8dd4670bd05'
down_revision = 'a7db9b22c525'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Show', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Show', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('Show_venue_id_fkey', 'Show', type_='foreignkey')
    op.drop_constraint('Show_artist_id_fkey', 'Show', type_='foreignkey')
    op.create_foreign_key(None, 'Show', 'Venue', ['venue_id'], ['id'])
    op.create_foreign_key(None, 'Show', 'Artist', ['artist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Show', type_='foreignkey')
    op.drop_constraint(None, 'Show', type_='foreignkey')
    op.create_foreign_key('Show_artist_id_fkey', 'Show', 'Artist', ['artist_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('Show_venue_id_fkey', 'Show', 'Venue', ['venue_id'], ['id'], ondelete='CASCADE')
    op.alter_column('Show', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Show', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
