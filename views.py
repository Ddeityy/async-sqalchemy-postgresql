from fastapi import APIRouter
from pydantic import BaseModel

from models import Order, User


class UserSchema(BaseModel):
    name: str
    surname: str


class UserSerializer(BaseModel):
    id: str
    name: str
    surname: str

    class Config:
        orm_mode = True


class OrderSchema(BaseModel):
    description: str
    customer: str


class OrderSerializer(BaseModel):
    id: str
    description: str
    customer: str

    class Config:
        orm_mode = True


users_api = APIRouter(
    prefix="/users",
)

orders_api = APIRouter(prefix="/orders")


@users_api.post("/", response_model=UserSerializer)
async def create_user(user: UserSchema):
    user = await User.create(**user.dict())
    return user


@orders_api.post("/")
async def create_order(order: OrderSchema):
    order = await Order.create(**order.dict())
    return order


@orders_api.get("/", response_model=list[OrderSerializer])
async def get_all_orders():
    orders = await Order.get_all()
    return orders


@users_api.get("/", response_model=list[UserSerializer])
async def get_all_users():
    users = await User.get_all()
    return users


@users_api.get("/{user_id}", response_model=UserSerializer)
async def get_user(user_id: str):
    user = await User.get(user_id)
    return user


@orders_api.get("/{order_id}", response_model=OrderSerializer)
async def get_order(order_id: str):
    order = await Order.get(order_id)
    return order


@users_api.put("/{user_id}", response_model=UserSerializer)
async def update(user_id: str, user: UserSchema):
    user = await User.update(user_id, **user.dict())
    return user


@users_api.delete("/{user_id}", response_model=bool)
async def delete_user(user_id: str):
    return await User.delete(user_id)


@users_api.get("/{user_id}/orders", response_model=list[OrderSerializer])
async def get_orders(user_id: str):
    orders = await Order.get_all_orders_by_user_id(user_id)
    return orders


@users_api.get("/{user_id}/orders/{order_id}", response_model=OrderSerializer)
async def get_order_by_user_id(user_id: str, order_id: str):
    order = await Order.get_order_by_user_id(user_id, order_id)
    return order
