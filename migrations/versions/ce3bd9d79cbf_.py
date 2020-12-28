"""empty message

Revision ID: ce3bd9d79cbf
Revises: 5e29f5d6540b
Create Date: 2020-12-28 12:14:09.636381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce3bd9d79cbf'
down_revision = '5e29f5d6540b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'predictions', ['photo', 'match'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'predictions', type_='unique')
    # ### end Alembic commands ###
