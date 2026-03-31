# models/item.py
from sqlalchemy import String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String(50), index=True)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
