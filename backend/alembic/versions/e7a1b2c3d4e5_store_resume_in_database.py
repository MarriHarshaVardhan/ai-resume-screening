"""store resume content in database

Revision ID: e7a1b2c3d4e5
Revises: d2f4c8b7a901
Create Date: 2026-08-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e7a1b2c3d4e5"
down_revision: Union[str, Sequence[str], None] = "d2f4c8b7a901"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("screenings", "resume_path", nullable=True)
    op.add_column("screenings", sa.Column("resume_content", sa.LargeBinary(), nullable=True))


def downgrade() -> None:
    op.drop_column("screenings", "resume_content")
    op.alter_column("screenings", "resume_path", nullable=False)
