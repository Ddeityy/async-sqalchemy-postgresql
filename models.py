from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, select, ForeignKey
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update

from database import Base, db


class User(Base):
    __tablename__ = "users"
    id = Column(String, unique=True, primary_key=True)
    name = Column(String)
    surname = Column(String)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"name={self.name}, "
            f"surname={self.surname}"
            f")>"
        )

    @classmethod
    async def create(cls, **kwargs):
        user = cls(id=str(uuid4()), **kwargs)
        db.add(user)

        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return user

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return await cls.get(id)

    @classmethod
    async def get_user(cls, id):
        query = select(cls).where(cls.id == id)
        users = await db.execute(query)
        (user,) = users.first()
        return user

    @classmethod
    async def get_all(cls):
        query = select(cls)
        users = await db.execute(query)
        users = users.scalars().all()
        return users

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True


class Order(Base):
    __tablename__ = "orders"
    id = Column(String, unique=True, primary_key=True)
    description = Column(String)
    customer = Column(String, ForeignKey("users.id"))

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"description={self.description}, "
            f"customer={self.customer}"
            f")>"
        )

    @classmethod
    async def get_order(cls, id):
        query = select(cls).where(cls.id == id)
        orders = await db.execute(query)
        (order,) = orders.first()
        return order

    @classmethod
    async def get_all(cls):
        query = select(cls)
        orders = await db.execute(query)
        orders = orders.scalars().all()
        return orders

    @classmethod
    async def create(cls, **kwargs):
        order = cls(id=str(uuid4()), **kwargs)
        db.add(order)

        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return order

    @classmethod
    async def get_all_orders_by_customer_id(cls, id):
        query = select(cls).where(cls.customer == id)
        orders = await db.execute(query)
        orders = orders.scalars().all()
        return orders

    @classmethod
    async def get_order_by_customer_id(cls, user_id, order_id):
        query = select(cls).where(cls.customer == user_id, cls.id == order_id)
        orders = await db.execute(query)
        (order,) = orders.first()
        return order
