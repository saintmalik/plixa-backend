from _decimal import Decimal
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, EmailStr


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
