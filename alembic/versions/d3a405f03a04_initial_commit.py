"""Initial Commit

Revision ID: d3a405f03a04
Revises: 
Create Date: 2020-02-09 09:37:59.783773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3a405f03a04'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    op.create_index('email_index', 'user', ['email'], unique=True, mysql_length=255)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('email_index', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
