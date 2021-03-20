"""empty message

Revision ID: 09c903ea5e2a
Revises: 820b53154452
Create Date: 2019-09-03 23:51:50.600599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09c903ea5e2a'
down_revision = '820b53154452'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('agenda_slug', sa.String(length=120), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contact', 'agenda_slug')
    # ### end Alembic commands ###