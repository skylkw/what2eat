from sqlalchemy import Integer, String, Text
from core.base_model import DateTimeMixin, Base
from sqlalchemy.orm import Mapped, mapped_column


class Dish(Base, DateTimeMixin):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
