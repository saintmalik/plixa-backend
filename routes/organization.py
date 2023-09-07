from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Security, HTTPException, status

from db import get_collection, DBCollection
from models import User, Organization, CreateOrganizationSchema
from routes.auth import get_current_user
from routes.cluster import cluster_router
from scopes import APIScope

organization_router = APIRouter(prefix="/organizations", tags=["organizations"])
organization_router.include_router(cluster_router)

organization_collection = get_collection(DBCollection.ORGANIZATION)
user_collection = get_collection(DBCollection.USER)


@organization_router.post("", status_code=status.HTTP_201_CREATED)
async def create_organization(
    user: Annotated[
        User,
        Security(get_current_user, scopes=[APIScope.ALL, APIScope.ORGANIZATION_WRITE]),
    ],
    organization_data: CreateOrganizationSchema,
):
    existing_organization = await organization_collection.find_one(
        {"name": organization_data.name}
    )
    if existing_organization:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="organization with this name already exists",
        )
    new_organization = await organization_collection.insert_one(
        organization_data.model_dump()
    )
    new_organization = await organization_collection.find_one(
        {"_id": new_organization.inserted_id}
    )
    return Organization.model_load(new_organization).model_dump()


@organization_router.get("")
async def get_organizations(
    user: Annotated[
        User,
        Security(get_current_user, scopes=[APIScope.ALL, APIScope.ORGANIZATION_READ]),
    ]
):
    organizations = []
    async for organization in organization_collection.find(
        {"members": {"$in": [str(user.id)]}}
    ):
        organizations.append(Organization.model_load(organization))
    return organizations


@organization_router.get("/{organization_id}")
async def get_organization(
    user: Annotated[
        User,
        Security(get_current_user, scopes=[APIScope.ALL, APIScope.ORGANIZATION_READ]),
    ],
    organization_id: str,
):
    organization = await organization_collection.find_one(
        {"_id": ObjectId(organization_id)}
    )
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"organization with id {organization_id} not found",
        )
    return Organization.model_load(organization).model_dump()


@organization_router.patch("/{organization_id}")
async def update_organization(
    user: Annotated[
        User,
        Security(get_current_user, scopes=[APIScope.ALL, APIScope.ORGANIZATION_WRITE]),
    ]
):
    ...


@organization_router.post("/{organization_id}/add-users")
async def add_users_to_organization(
    user: Annotated[
        User,
        Security(get_current_user, scopes=[APIScope.ALL, APIScope.ORGANIZATION_WRITE]),
    ],
    organization_id: str,
    user_ids: list[str],
):
    organization_in_db = await organization_collection.find_one(
        {"_id": ObjectId(organization_id)}
    )
    if not organization_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"organization with id {organization_id} not found",
        )
    organization = Organization.model_load(organization_in_db)
    users: list[User] = []
    async for user_in_db in user_collection.find(
        {"_id": {"$in": [ObjectId(user_id) for user_id in user_ids]}}
    ):
        users.append(User.model_load(user_in_db))
    valid_user_ids = [user.id for user in users]
    new_members = list(set(organization.members).union(set(valid_user_ids)))
    result = await organization_collection.update_one(
        {"_id": ObjectId(organization_id)}, {"$set": {"members": new_members}}
    )
    organization_in_db = await organization_collection.find_one(
        {"_id": ObjectId(organization_id)}
    )
    return Organization.model_load(organization_in_db)


@organization_router.post("/{organization_id}/remove-users")
async def remove_users_remove_organization(
    user: Annotated[
        User,
        Security(get_current_user, scopes=[APIScope.ALL, APIScope.ORGANIZATION_WRITE]),
    ],
    organization_id: str,
    user_ids: list[str],
):
    organization_in_db = await organization_collection.find_one(
        {"_id": ObjectId(organization_id)}
    )
    if not organization_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"organization with id {organization_id} not found",
        )
    organization = Organization.model_load(organization_in_db)
    users: list[User] = []
    async for user_in_db in user_collection.find(
        {"_id": {"$in": [ObjectId(user_id) for user_id in user_ids]}}
    ):
        users.append(User.model_load(user_in_db))
    valid_user_ids = [user.id for user in users]
    new_members = list(set(organization.members).difference(set(valid_user_ids)))
    result = await organization_collection.update_one(
        {"_id": ObjectId(organization_id)}, {"$set": {"members": new_members}}
    )
    organization_in_db = await organization_collection.find_one(
        {"_id": ObjectId(organization_id)}
    )
    return Organization.model_load(organization_in_db)


@organization_router.delete(
    "/{organization_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_organization(
    user: Annotated[
        User,
        Security(get_current_user, scopes=[APIScope.ALL, APIScope.ORGANIZATION_WRITE]),
    ]
):
    ...
