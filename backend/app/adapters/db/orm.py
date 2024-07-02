import sqlalchemy as sa
from sqlalchemy.orm import registry
from sqlalchemy.sql import func

import app.domain.entities as models

metadata = sa.MetaData()
mapper_registry = registry(metadata=metadata)


users = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column("email", sa.String, primary_key=True, index=True),
    sa.Column("hashed_password", sa.String, nullable=False),
    sa.Column("username", sa.String, nullable=False),
    sa.Column("date_of_birth", sa.Date, nullable=False),
    sa.Column("gender", sa.String, nullable=False),
    sa.Column("phone_number", sa.String, nullable=False, index=True),
    sa.Column("resume_file_id", sa.String, nullable=True),
    sa.Column("status", sa.String, nullable=True, index=True),
    sa.Column("role", sa.String, nullable=False, index=True),
    sa.Column("created_at", sa.DateTime, server_default=func.now(), index=True),
    sa.Column("updated_at", sa.DateTime, onupdate=func.now(), index=True),
)

user_auth_codes = sa.Table(
    "user_auth_codes",
    mapper_registry.metadata,
    sa.Column("id", sa.String, primary_key=True, index=True),
    sa.Column("email", sa.String, nullable=False, index=True),
    sa.Column("auth_code", sa.String, nullable=False, index=True),
    sa.Column("expired_at", sa.DateTime, nullable=False),
    sa.Column("status", sa.String, nullable=True, index=True),
    sa.Column("created_at", sa.DateTime, server_default=func.now(), index=True),
    sa.Column("updated_at", sa.DateTime, onupdate=func.now(), index=True),
)

files = sa.Table(
    "files",
    mapper_registry.metadata,
    sa.Column("id", sa.String, primary_key=True, index=True),
    sa.Column("category", sa.String, nullable=False, index=True),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("extension", sa.String, nullable=False, index=True),
    sa.Column("url", sa.String, nullable=False),
    sa.Column("is_deleted", sa.Boolean(), default=False),
    sa.Column("created_at", sa.DateTime, server_default=func.now(), index=True),
    sa.Column("updated_at", sa.DateTime, onupdate=func.now(), index=True),
)


def start_mappers() -> None:
    for entity, table in {
        models.User: users,
        models.UserAuthCode: user_auth_codes,
        models.File: files,
    }.items():
        mapper_registry.map_imperatively(entity, table)
