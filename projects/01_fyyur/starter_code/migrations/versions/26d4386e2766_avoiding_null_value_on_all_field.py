"""avoiding null value on all field

Revision ID: 26d4386e2766
Revises: 9d6f296fb7d8
Create Date: 2022-06-06 07:37:09.714639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26d4386e2766'
down_revision = '9d6f296fb7d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Artist', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Artist', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Artist', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Artist', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('Artist', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Artist', 'website_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Venue', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('Venue', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Venue', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Venue', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('Venue', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Venue', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Venue', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Venue', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Venue', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('Artist', 'website_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Artist', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Artist', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('Artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Artist', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Artist', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Artist', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Artist', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###