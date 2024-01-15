from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .product import Product


class Order(Base):
    __tablename__ = "orders"

    promocode: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    products: Mapped[list["Product"]] = relationship(
        secondary="order_product_association",
        back_populates="orders",
    )
