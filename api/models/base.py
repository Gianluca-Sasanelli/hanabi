"""Base model for SQLAlchemy models."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ruff: noqa: UP017


class Base(DeclarativeBase):

    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.key)
            if isinstance(value, UUID):
                result[column.key] = str(value)
            elif isinstance(value, datetime):
                if value.tzinfo is None:
                    value = value.replace(tzinfo=timezone.utc)
                result[column.key] = value.isoformat()
            else:
                result[column.key] = value
        return result

    @classmethod
    def to_dict_list(cls, models):
        return [model.to_dict() for model in models] if models else []
