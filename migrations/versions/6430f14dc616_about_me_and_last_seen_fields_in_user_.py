"""about_me and last_seen fields in user model

Revision ID: 6430f14dc616
Revises: 85311d8095de
Create Date: 2018-09-08 12:03:14.759095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6430f14dc616'
down_revision = '85311d8095de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('users', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_seen')
    op.drop_column('users', 'about_me')
    # ### end Alembic commands ###