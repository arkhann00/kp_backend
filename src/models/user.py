# src/models/user.py
from sqlalchemy import JSON, String, Boolean, Enum, Table, Integer, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from src.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product

# Таблица связей many-to-many
favorites_table = Table(
    "favorites",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
    Column("product_id", Integer, ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
)


class UserRole(enum.Enum):
    BUYER = "buyer"
    ADMIN = "admin"

    
class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    username: Mapped[str | None] = mapped_column(String(255))
    first_name: Mapped[str | None] = mapped_column(String(255))
    second_name: Mapped[str | None] = mapped_column(String(255))
    image_url: Mapped[str | None] = mapped_column(String(512))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.BUYER, nullable=False)
    
    favorite_product_ids: Mapped[list[int]] = mapped_column(JSON, default=list)
