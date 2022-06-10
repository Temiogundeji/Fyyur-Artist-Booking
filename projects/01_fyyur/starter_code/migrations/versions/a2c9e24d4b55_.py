"""empty message

Revision ID: a2c9e24d4b55
Revises: 956b036bc38a
Create Date: 2022-06-04 06:46:57.662307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2c9e24d4b55'
down_revision = '956b036bc38a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('created', sa.DateTime(), nullable=True))
    op.add_column('Artist', sa.Column('updated', sa.DateTime(), nullable=True))
    op.add_column('Venue', sa.Column('created', sa.DateTime(), nullable=False))
    op.add_column('Venue', sa.Column('updated', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'updated')
    op.drop_column('Venue', 'created')
    op.drop_column('Artist', 'updated')
    op.drop_column('Artist', 'created')
    op.create_table('show',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='show_pkey')
    )
    op.create_table('Shows',
    sa.Column('venue.id', sa.INTEGER(), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###