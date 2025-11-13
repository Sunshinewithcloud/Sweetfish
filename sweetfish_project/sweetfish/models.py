"""Module adjusted to satisfy style checks."""

from __future__ import annotations

import datetime
import enum
import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple


def gen_id(prefix: str = "") -> str:
    unique_id = uuid.uuid4()
    short_id = unique_id.hex[:12]
    final_id = prefix + short_id
    return final_id


class Role(enum.Enum):

    BUYER = "buyer"
    MERCHANT = "merchant"
    ADMIN = "admin"


@dataclass
class BaseUser:

    user_id: str
    phone: str
    name: str
    role: Role = Role.BUYER
    created_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    password_hash: Optional[str] = None

    def __repr__(self) -> str:
        return f"<User {self.user_id} {self.name} {self.role.value}>"


@dataclass
class Merchant(BaseUser):

    shop_name: str = ""
    verified: bool = False
    shop_description: Optional[str] = None

    def __post_init__(self) -> None:
        self.role = Role.MERCHANT


@dataclass
class Admin(BaseUser):

    privileges: Set[str] = field(default_factory=lambda: {"all"})

    # 对象初始化后自动调用，将属性设置为管理员
    def __post_init__(self) -> None:
        self.role = Role.ADMIN


@dataclass
class Product:

    product_id: str
    merchant_id: str
    title: str
    description: str
    price_cents: int
    stock: int = 0
    allow_bargain: bool = True
    views: int = 0
    sold: int = 0
    promotion_rank: int = 0
    tags: Set[str] = field(default_factory=set)
    created_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)

    def is_available(self) -> bool:
        return self.stock > 0


@dataclass
class OrderItem:

    product_id: str
    quantity: int


class OrderStatus(enum.Enum):

    CREATED = "created"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


@dataclass
class Order:

    order_id: str
    buyer_id: str
    merchant_id: str
    items: List[OrderItem]
    total_cents: int
    status: OrderStatus = OrderStatus.CREATED
    created_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    payment_id: Optional[str] = None

    def mark_paid(self, payment_id: str) -> None:

        self.payment_id = payment_id
        self.status = OrderStatus.PAID
        self.updated_at = datetime.datetime.utcnow()


@dataclass
class Payment:

    payment_id: str
    order_id: str
    amount_cents: int
    provider: str = "BliPay"
    status: str = "init"
    created_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)


@dataclass
class Bargain:


    bargain_id: str
    product_id: str
    requester_id: str
    original_price_cents: int
    current_price_cents: int
    participants: Set[str] = field(default_factory=set)
    expires_at: Optional[datetime.datetime] = None
    closed: bool = False


@dataclass
class Review:


    review_id: str
    product_id: str
    user_id: str
    rating: int
    comment: str
    created_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
