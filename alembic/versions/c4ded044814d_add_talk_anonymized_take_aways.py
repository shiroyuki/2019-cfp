"""add Talk.anonymized_take_aways

Revision ID: c4ded044814d
Revises: 224984e82a90
Create Date: 2019-05-13 04:48:07.957509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4ded044814d'
down_revision = '224984e82a90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('talk', sa.Column('anonymized_take_aways', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('talk', 'anonymized_take_aways')
    # ### end Alembic commands ###
