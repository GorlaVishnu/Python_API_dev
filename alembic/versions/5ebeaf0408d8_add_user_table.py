"""add user table

Revision ID: 5ebeaf0408d8
Revises: 746ffb82edf0
Create Date: 2025-03-11 12:29:47.008677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ebeaf0408d8'
down_revision: Union[str, None] = '746ffb82edf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users', 
                    sa.Column('Id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('Id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    
