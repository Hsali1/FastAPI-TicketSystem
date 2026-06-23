from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None,
    )

    # posts: Mapped[list[Post]] = relationship(back_populates="author")
    # tickets: Mapped[list[Ticket]] = relationship(back_populates="author")
    created_tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="created_by",
        foreign_keys="Ticket.created_by_id",
    )

    assigned_tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="assigned_to",
        foreign_keys="Ticket.assigned_to_id",
    )


    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="Open")

    created_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    assigned_to_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    created_by: Mapped["User"] = relationship(
        back_populates="created_tickets",
        foreign_keys=[created_by_id],
    )

    assigned_to: Mapped["User | None"] = relationship(
        back_populates="assigned_tickets",
        foreign_keys=[assigned_to_id],
    )