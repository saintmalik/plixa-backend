from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class Withdrawal(BaseModel):
    id: str | None = Field(...)
    reference: str  # The transaction reference of the withdrawal
    beneficiary: str
    amount: Decimal
    created_at: datetime = Field(default_factory=datetime.now)
