"""Initial Migration

Revision ID: e2912aa713a6
Revises: 
Create Date: 2022-11-17 02:15:06.729882

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e2912aa713a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.alter_column('groupName',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=64),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.alter_column('groupName',
               existing_type=sa.String(length=64),
               type_=mysql.VARCHAR(length=45),
               existing_nullable=True)

    # ### end Alembic commands ###
