"""add screenings table

Revision ID: d2f4c8b7a901
Revises: c95651a037c7
Create Date: 2026-08-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d2f4c8b7a901"
down_revision: Union[str, Sequence[str], None] = "c95651a037c7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "screenings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("job_title", sa.String(length=255), nullable=False),
        sa.Column("required_skills", sa.Text(), nullable=False),
        sa.Column("resume_filename", sa.String(length=255), nullable=False),
        sa.Column("resume_path", sa.String(length=500), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_screenings_id"), "screenings", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_screenings_id"), table_name="screenings")
    op.drop_table("screenings")
