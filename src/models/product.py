from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum
from src.models.base import Base

class Product(Base):
    __tablename__ = "product"
    
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column()
    
    image_url: Mapped[str] = mapped_column(nullable=True)
    
    discont: Mapped[int] = mapped_column(nullable=True)
    category: Mapped[str] = mapped_column(nullable=True)
    ozon_url: Mapped[str] = mapped_column(nullable=True)
    wildberries_url: Mapped[str] = mapped_column(nullable=True)