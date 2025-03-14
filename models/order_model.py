from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    order_items = Column(String, nullable=False)
    table_number = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Order(id={self.id}, customer_name='{self.customer_name}', table_number={self.table_number})>"