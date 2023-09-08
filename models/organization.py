from pydantic import BaseModel

from models.user import User


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
