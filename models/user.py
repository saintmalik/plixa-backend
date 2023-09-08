from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr

from db import get_collection, DBCollection
from utils.auth import verify_password


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
