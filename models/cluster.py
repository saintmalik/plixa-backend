from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


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
    # additional information about what bills the cluster is trying to collect
    description: str | None
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
