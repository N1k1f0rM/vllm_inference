import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    create_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

