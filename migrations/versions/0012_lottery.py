"""lottery

Revision ID: 0012
Revises: 0011
Create Date: 2025-01-11 10:44:55.094381

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0012"
down_revision: str | None = "0011"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("student_id", sa.String(length=8), nullable=True))
    op.add_column("users", sa.Column("group", sa.String(length=10), nullable=True))
    op.create_unique_constraint(op.f("uq_users_student_id"), "users", ["student_id"])
    op.drop_column("users", "stage")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("stage", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(op.f("uq_users_student_id"), "users", type_="unique")
    op.drop_column("users", "group")
    op.drop_column("users", "student_id")
    # ### end Alembic commands ###