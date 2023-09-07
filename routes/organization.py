from typing import Annotated

from fastapi import APIRouter, Security

from models import User
from routes.auth import get_current_user

organization_router = APIRouter(prefix="/organizations")


@organization_router.post("")
async def create_organization(
    user: Annotated[
        User, Security(get_current_user, scopes=["all", "organization:write"])
    ]
):
    ...


@organization_router.get("")
async def get_organization():
    ...
