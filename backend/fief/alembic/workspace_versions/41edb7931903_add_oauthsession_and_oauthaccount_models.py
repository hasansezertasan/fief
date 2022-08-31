"""Add OAuthSession and OAuthAccount models

Revision ID: 41edb7931903
Revises: b2b8a6110627
Create Date: 2022-07-13 10:28:46.360444

"""
import sqlalchemy as sa
from alembic import op

import fief

# revision identifiers, used by Alembic.
revision = "41edb7931903"
down_revision = "b2b8a6110627"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "fief_oauth_accounts",
        sa.Column("id", fief.models.generics.GUID(), nullable=False),
        sa.Column(
            "created_at",
            fief.models.generics.TIMESTAMPAware(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            fief.models.generics.TIMESTAMPAware(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("access_token", sa.Text(), nullable=False),
        sa.Column(
            "expires_at",
            fief.models.generics.TIMESTAMPAware(timezone=True),
            nullable=True,
        ),
        sa.Column("refresh_token", sa.Text(), nullable=True),
        sa.Column("account_id", sa.String(length=1024), nullable=False),
        sa.Column("account_email", sa.String(length=1024), nullable=False),
        sa.Column("oauth_provider_id", fief.models.generics.GUID(), nullable=False),
        sa.Column("user_id", fief.models.generics.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["oauth_provider_id"], ["fief_oauth_providers.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["fief_users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("oauth_provider_id", "user_id"),
    )
    op.create_index(
        op.f("ix_fief_oauth_accounts_account_id"),
        "fief_oauth_accounts",
        ["account_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_fief_oauth_accounts_created_at"),
        "fief_oauth_accounts",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_fief_oauth_accounts_updated_at"),
        "fief_oauth_accounts",
        ["updated_at"],
        unique=False,
    )
    op.create_table(
        "fief_oauth_sessions",
        sa.Column("id", fief.models.generics.GUID(), nullable=False),
        sa.Column(
            "created_at",
            fief.models.generics.TIMESTAMPAware(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            fief.models.generics.TIMESTAMPAware(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("redirect_uri", sa.Text(), nullable=False),
        sa.Column("oauth_provider_id", fief.models.generics.GUID(), nullable=False),
        sa.Column("login_session_id", fief.models.generics.GUID(), nullable=False),
        sa.Column(
            "expires_at",
            fief.models.generics.TIMESTAMPAware(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["login_session_id"], ["fief_login_sessions.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["oauth_provider_id"], ["fief_oauth_providers.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_fief_oauth_sessions_created_at"),
        "fief_oauth_sessions",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_fief_oauth_sessions_expires_at"),
        "fief_oauth_sessions",
        ["expires_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_fief_oauth_sessions_token"),
        "fief_oauth_sessions",
        ["token"],
        unique=True,
    )
    op.create_index(
        op.f("ix_fief_oauth_sessions_updated_at"),
        "fief_oauth_sessions",
        ["updated_at"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_fief_oauth_sessions_updated_at"), table_name="fief_oauth_sessions"
    )
    op.drop_index(
        op.f("ix_fief_oauth_sessions_token"), table_name="fief_oauth_sessions"
    )
    op.drop_index(
        op.f("ix_fief_oauth_sessions_expires_at"), table_name="fief_oauth_sessions"
    )
    op.drop_index(
        op.f("ix_fief_oauth_sessions_created_at"), table_name="fief_oauth_sessions"
    )
    op.drop_table("fief_oauth_sessions")
    op.drop_index(
        op.f("ix_fief_oauth_accounts_updated_at"), table_name="fief_oauth_accounts"
    )
    op.drop_index(
        op.f("ix_fief_oauth_accounts_created_at"), table_name="fief_oauth_accounts"
    )
    op.drop_index(
        op.f("ix_fief_oauth_accounts_account_id"), table_name="fief_oauth_accounts"
    )
    op.drop_table("fief_oauth_accounts")
    # ### end Alembic commands ###
