from fastapi import APIRouter

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.patch("/{user_id}")
async def update_user(user_id: str):
    ...


@user_router.post("/{user_id}")
async def disable_user(user_id: str):
    ...


@user_router.delete("/{user_id}")
async def delete_user(user_id: str):
    ...
