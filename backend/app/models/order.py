from sqlalchemy import Column, ForeignKey, Integer, DateTime, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base
from schemas.order import OrderStatus


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(OrderStatus))

    items = relationship("OrderItem", back_populates="order")
    staff = relationship("Staff")


class OrderItem(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    qty = Column(Integer)
    menu_id = Column(Integer, ForeignKey("menu.id"))
    price_unit = Column(Numeric(12, 2))
    price_total = Column(Numeric(12, 2))
    cost_unit = Column(Numeric(12, 2))
    cost_total = Column(Numeric(12, 2))

    order = relationship("Order", back_populates="items")
    menu = relationship("Menu")
