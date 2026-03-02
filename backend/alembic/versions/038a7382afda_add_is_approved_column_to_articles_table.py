"""Add is_approved column to articles table

Revision ID: 038a7382afda
Revises: 5b5e1bdc0b95
Create Date: 2026-02-24 19:01:35.758016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '038a7382afda'
down_revision = '5b5e1bdc0b95'
branch_labels = None
depends_on = None


def upgrade():
    # Only add is_approved column, skip other changes that SQLite doesn't support
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_approved', sa.Boolean(), nullable=False, server_default=sa.text('1')))


def downgrade():
    # Only drop is_approved column, skip other changes
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.drop_column('is_approved')
