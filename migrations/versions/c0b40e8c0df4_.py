"""empty message

Revision ID: c0b40e8c0df4
Revises: 
Create Date: 2023-04-09 14:24:26.590803

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "c0b40e8c0df4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "forum_categories",
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("type", sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "forum_tags",
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "player_stats",
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("points", sa.Integer(), nullable=True),
        sa.Column("kills", sa.Integer(), nullable=True),
        sa.Column("deaths", sa.Integer(), nullable=True),
        sa.Column("assists", sa.Integer(), nullable=True),
        sa.Column("damage", sa.Integer(), nullable=True),
        sa.Column("damage_taken", sa.Integer(), nullable=True),
        sa.Column("healing", sa.Integer(), nullable=True),
        sa.Column("healing_taken", sa.Integer(), nullable=True),
        sa.Column("headshots", sa.Integer(), nullable=True),
        sa.Column("backstabs", sa.Integer(), nullable=True),
        sa.Column("dominations", sa.Integer(), nullable=True),
        sa.Column("revenges", sa.Integer(), nullable=True),
        sa.Column("captures", sa.Integer(), nullable=True),
        sa.Column("defends", sa.Integer(), nullable=True),
        sa.Column("ubers", sa.Integer(), nullable=True),
        sa.Column("teleports", sa.Integer(), nullable=True),
        sa.Column("suicides", sa.Integer(), nullable=True),
        sa.Column("sentries", sa.Integer(), nullable=True),
        sa.Column("buildings_destroyed", sa.Integer(), nullable=True),
        sa.Column("buildings_destroyed_sentry", sa.Integer(), nullable=True),
        sa.Column("buildings_destroyed_dispenser", sa.Integer(), nullable=True),
        sa.Column("buildings_destroyed_teleporter", sa.Integer(), nullable=True),
        sa.Column("time_played", sa.Integer(), nullable=True),
        sa.Column("last_time_played", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("color", sa.String(length=256), nullable=True),
        sa.Column("is_staff", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "scopes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("app_name", sa.String(length=64), nullable=False),
        sa.Column("value", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=256), nullable=False),
        sa.Column("protected", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "servers",
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("ip", sa.String(length=64), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ip"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "steamrep_profiles",
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_url", sa.String(length=255), nullable=False),
        sa.Column("is_scammer", sa.Boolean(), nullable=True),
        sa.Column("steamid64", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("profile_url"),
        sa.UniqueConstraint("steamid64"),
    )
    op.create_table(
        "roles_scopes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scope", sa.Integer(), nullable=True),
        sa.Column("role", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["role"],
            ["roles.id"],
            name="fk_roles_scopes_roles_role_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["scope"],
            ["scopes.id"],
            name="fk_roles_scopes_scopes_scope_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("is_activated", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.Column("avatar", sa.String(length=255), nullable=True),
        sa.Column("display_role", sa.Integer(), nullable=True),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.Column("secret_salt", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["display_role"], ["roles.id"], name="fk_users_roles_id_display_role"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("secret_salt"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "apps",
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=100), nullable=False),
        sa.Column("owner", sa.Integer(), nullable=True),
        sa.Column("is_activated", sa.Boolean(), nullable=True),
        sa.Column("client_id", sa.String(length=16), nullable=True),
        sa.Column("client_secret", sa.String(length=50), nullable=True),
        sa.Column("secret_key", sa.String(length=32), nullable=True),
        sa.ForeignKeyConstraint(["owner"], ["users.id"], name="fk_apps_users_id_owner"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "banned",
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user", sa.Integer(), nullable=True),
        sa.Column("reason", sa.String(length=255), nullable=False),
        sa.Column("ban_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("banned_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["banned_by"], ["users.id"], name="fk_banned_users_id_banned_by"
        ),
        sa.ForeignKeyConstraint(["user"], ["users.id"], name="fk_banned_users_id_user"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "chats",
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("author", sa.Integer(), nullable=True),
        sa.Column("message", sa.String(length=500), nullable=False),
        sa.ForeignKeyConstraint(
            ["author"], ["users.id"], name="fk_chats_users_id_author"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "forum_posts",
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("author", sa.Integer(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author"], ["users.id"], name="fk_forum_posts_users_id_author"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "forum_threads",
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=64), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("is_closed", sa.Boolean(), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=True),
        sa.Column("category", sa.Integer(), nullable=True),
        sa.Column("author", sa.Integer(), nullable=True),
        sa.Column("server", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["author"], ["users.id"], name="fk_forum_threads_users_id_author"
        ),
        sa.ForeignKeyConstraint(
            ["category"],
            ["forum_categories.id"],
            name="fk_forum_threads_forum_categories_id_category",
        ),
        sa.ForeignKeyConstraint(
            ["server"], ["servers.id"], name="fk_forum_threads_servers_id_server"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "players",
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user", sa.Integer(), nullable=True),
        sa.Column("steamrep_profile", sa.Integer(), nullable=True),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("steamid3", sa.String(length=255), nullable=False),
        sa.Column("steamid32", sa.String(length=255), nullable=False),
        sa.Column("steamid64", sa.String(length=255), nullable=False),
        sa.Column("profile_url", sa.String(length=255), nullable=True),
        sa.Column("avatar", sa.String(length=255), nullable=True),
        sa.Column("country_code", sa.String(length=15), nullable=False),
        sa.Column("reputation", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["steamrep_profile"],
            ["steamrep_profiles.id"],
            name="fk_players_steamrep_profiles_id_steamrep_profile",
        ),
        sa.ForeignKeyConstraint(
            ["user"], ["users.id"], name="fk_players_users_id_user"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("profile_url"),
        sa.UniqueConstraint("steamid3"),
        sa.UniqueConstraint("steamid32"),
        sa.UniqueConstraint("steamid64"),
    )
    op.create_table(
        "users_roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("role", sa.Integer(), nullable=True),
        sa.Column("user", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["role"],
            ["roles.id"],
            name="fk_users_roles_roles_role_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user"],
            ["users.id"],
            name="fk_users_roles_users_user_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "apps_scopes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scope", sa.Integer(), nullable=True),
        sa.Column("app", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["app"],
            ["apps.id"],
            name="fk_apps_scopes_apps_app_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["scope"],
            ["scopes.id"],
            name="fk_apps_scopes_scopes_scope_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "server_stats",
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("server", sa.Integer(), nullable=True),
        sa.Column("player", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["player"], ["players.id"], name="fk_server_stats_players_id_player"
        ),
        sa.ForeignKeyConstraint(
            ["server"], ["servers.id"], name="fk_server_stats_servers_id_server"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "threads_posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("post", sa.Integer(), nullable=True),
        sa.Column("thread", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["post"],
            ["forum_posts.id"],
            name="fk_threads_posts_forum_posts_post_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["thread"],
            ["forum_threads.id"],
            name="fk_threads_posts_forum_threads_thread_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "threads_tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tag", sa.Integer(), nullable=True),
        sa.Column("thread", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tag"],
            ["forum_tags.id"],
            name="fk_threads_tags_forum_tags_tag_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["thread"],
            ["forum_threads.id"],
            name="fk_threads_tags_forum_threads_thread_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "serverplayerstatss_playerstatss",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("playerstats", sa.Integer(), nullable=True),
        sa.Column("serverplayerstats", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["playerstats"],
            ["player_stats.id"],
            name="fk_sps_player_stats_player_stats_player_stats_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["serverplayerstats"],
            ["server_stats.id"],
            name="fk_sps_stats_server_stats_server_player_stats_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("serverplayerstatss_playerstatss")
    op.drop_table("threads_tags")
    op.drop_table("threads_posts")
    op.drop_table("server_stats")
    op.drop_table("apps_scopes")
    op.drop_table("users_roles")
    op.drop_table("players")
    op.drop_table("forum_threads")
    op.drop_table("forum_posts")
    op.drop_table("chats")
    op.drop_table("banned")
    op.drop_table("apps")
    op.drop_table("users")
    op.drop_table("roles_scopes")
    op.drop_table("steamrep_profiles")
    op.drop_table("servers")
    op.drop_table("scopes")
    op.drop_table("roles")
    op.drop_table("player_stats")
    op.drop_table("forum_tags")
    op.drop_table("forum_categories")
    # ### end Alembic commands ###