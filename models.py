from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from db import DBCollection, get_collection
from utils import verify_password


class UserType(str, Enum):
    PLIXA_SUPERUSER = "plixa_superuser"
    PLIXA_STAFF = (
        "plixa_staff"  # for compliance and creation of platform users and organization
    )
    PLATFORM_USER = "platform_user"


class User(BaseModel):
    id: str | None = None
    type: UserType
    email: EmailStr
    first_name: str
    last_name: str
    password: str  # hashed

    @classmethod
    def model_load(cls, db_model: dict) -> "User":
        return User(
            id=str(db_model["_id"]),
            type=db_model["type"],
            email=db_model["email"],
            first_name=db_model["first_name"],
            last_name=db_model["last_name"],
            password=db_model["password"],
        )

    @classmethod
    async def authenticate(cls, email, password: str) -> Optional["User"]:
        user_collection = get_collection(DBCollection.USER)
        user = await user_collection.find_one({"email": email})
        is_correct_password = False
        if user:
            is_correct_password = verify_password(password, user["password"])
        if is_correct_password:
            return User.model_load(user)


class CreateUserSchema(BaseModel):
    type: UserType
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    confirm_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "type": UserType.PLATFORM_USER,
                "email": "johndoe@example.com",
                "first_name": "john",
                "last_name": "doe",
                "password": "password123",
                "confirm_password": "password123",
            }
        }


class UserSchema(BaseModel):
    id: str | None = None
    type: UserType
    email: EmailStr
    first_name: str
    last_name: str


class Organization(BaseModel):
    id: str | None = None
    name: str
    members: list[str]

    @classmethod
    def model_load(cls, db_model: dict) -> "Organization":
        return Organization(
            id=str(db_model["_id"]),
            name=db_model["name"],
            members=db_model["members"],
        )

    def is_member(self, user: User) -> bool:
        return user.id in self.members


class CreateOrganizationSchema(BaseModel):
    name: str
    members: list[str] | None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ekiti State University SUG",
                "members": [],
            }
        }


class AcceptablePayment(str, Enum):
    FULL = "full"
    HALF = "half"
    QUARTER = "quarter"


class ClusterStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    EXPIRED = "expired"


class Cluster(BaseModel):
    """A cluster is basically a payment collection that allows an
    organization to accept payments"""

    id: str | None = Field(...)
    organization_id: str  # The organization the cluster belongs to.
    name: str  # The name of the payment cluster
    description: str | None  # additional information about what bills the cluster is trying to collect
    amount: Decimal
    min_acceptable_payment: AcceptablePayment
    status: ClusterStatus = Field(ClusterStatus.DRAFT)
    expires_at: datetime | None
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def model_load(cls, db_model: dict) -> "Cluster":
        return Cluster(
            id=str(db_model["_id"]),
            organization_id=db_model["organization_id"],
            name=db_model["name"],
            description=db_model["description"],
            amount=db_model["amount"],
            min_acceptable_payment=db_model["min_acceptable_payment"],
            status=db_model["status"],
            expires_at=db_model["expires_at"],
            created_at=db_model["created_at"],
        )


class CreateClusterSchema(BaseModel):
    name: str
    description: str | None
    amount: Decimal
    min_acceptable_payment: AcceptablePayment

    class Config:
        json_schema_extra = {
            "example": {
                "name": "SUG Union Due Staylites",
                "amount": 800,
                "min_acceptable_payment": AcceptablePayment.FULL,
            }
        }


class Withdrawal(BaseModel):
    id: str | None = Field(...)
    reference: str  # The transaction reference of the withdrawal
    beneficiary: str
    amount: Decimal
    created_at: datetime = Field(default_factory=datetime.now)


class TransactionStatus(str, Enum):
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"


class Transaction(BaseModel):
    id: str | None = Field(...)
    reference: str
    email: EmailStr
    amount: Decimal
    status: TransactionStatus = Field(TransactionStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.now)
