"""empty message

Revision ID: ce97522d6235
Revises:
Create Date: 2023-01-22 16:16:50.236189

"""
import sqlalchemy as sa
from alembic import op

revision = "ce97522d6235"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "menus",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("submenus_count", sa.Integer(), nullable=True),
        sa.Column("dishes_count", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(op.f("ix_menus_title"), "menus", ["title"], unique=False)
    op.create_table(
        "submenus",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("dishes_count", sa.Integer(), nullable=True),
        sa.Column("menu_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["menu_id"],
            ["menus.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(
        op.f("ix_submenus_title"), "submenus", ["title"], unique=False
    )
    op.create_table(
        "dishes",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.String(), nullable=False),
        sa.Column("submenu_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["submenu_id"],
            ["submenus.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(op.f("ix_dishes_title"), "dishes", ["title"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_dishes_title"), table_name="dishes")
    op.drop_table("dishes")
    op.drop_index(op.f("ix_submenus_title"), table_name="submenus")
    op.drop_table("submenus")
    op.drop_index(op.f("ix_menus_title"), table_name="menus")
    op.drop_table("menus")
