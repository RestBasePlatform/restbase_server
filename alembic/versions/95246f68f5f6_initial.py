"""initial

Revision ID: 95246f68f5f6
Revises:
Create Date: 2021-09-08 16:14:32.120850

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "95246f68f5f6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "groups",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("user_list", sa.String(), nullable=False),
        sa.Column("comment", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "secret",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("secret", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "submodule",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("functions", sa.JSON(), nullable=False),
        sa.Column("min_module_version", sa.String(), nullable=False),
        sa.Column("release_date", sa.DateTime(), nullable=False),
        sa.Column("files_url", sa.String(), nullable=False),
        sa.Column("database_type", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "database_connection",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username_secret_id", sa.Integer(), nullable=True),
        sa.Column("password_secret_id", sa.Integer(), nullable=True),
        sa.Column("host_secret_id", sa.Integer(), nullable=True),
        sa.Column("port_secret_id", sa.Integer(), nullable=True),
        sa.Column("connection_kwargs", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(
            ["host_secret_id"],
            ["secret.id"],
        ),
        sa.ForeignKeyConstraint(
            ["password_secret_id"],
            ["secret.id"],
        ),
        sa.ForeignKeyConstraint(
            ["port_secret_id"],
            ["secret.id"],
        ),
        sa.ForeignKeyConstraint(
            ["username_secret_id"],
            ["secret.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username_secret_id", sa.Integer(), nullable=True),
        sa.Column("password_secret_id", sa.Integer(), nullable=True),
        sa.Column("comment", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["password_secret_id"],
            ["secret.id"],
        ),
        sa.ForeignKeyConstraint(
            ["username_secret_id"],
            ["secret.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "installation",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("installation_date", sa.DateTime(), nullable=False),
        sa.Column("submodule_id", sa.Integer(), nullable=False),
        sa.Column("connection_data_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["connection_data_id"],
            ["database_connection.id"],
        ),
        sa.ForeignKeyConstraint(
            ["submodule_id"],
            ["submodule.id"],
        ),
        sa.PrimaryKeyConstraint("name"),
    )
    op.create_table(
        "database_list",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("installation", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["installation"],
            ["installation.name"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "schema_list",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("database", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["database"],
            ["database_list.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "table_list",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("schema", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["schema"],
            ["schema_list.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "column_list",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("datatype", sa.String(), nullable=True),
        sa.Column("table", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["table"],
            ["table_list.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("column_list")
    op.drop_table("table_list")
    op.drop_table("schema_list")
    op.drop_table("database_list")
    op.drop_table("installation")
    op.drop_table("users")
    op.drop_table("database_connection")
    op.drop_table("submodule")
    op.drop_table("secret")
    op.drop_table("groups")
    # ### end Alembic commands ###
