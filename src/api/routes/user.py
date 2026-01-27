from fastapi import APIRouter
from src.api.schemas.user import UserCreate
from src.db.repositories.user import (create_user, add_favorite_product, remove_favorite_product, get_favorite_products_for_user)
from src.dependencies import SessionDep

router = APIRouter()

@router.post("/user")
async def register_user(new_user: UserCreate):
    await create_user(session=SessionDep, new_user_schema=new_user)
    return "success"

@router.put("/user/favorite")
async def update_favorite_product(user_id: int,product_id: int):
    await add_favorite_product(session=SessionDep, user_id=user_id, favorite_product_id=product_id)
    return "success"

@router.delete("user/favorite")
async def delete_favorite_product(user_id: int,product_id: int):
    remove_favorite_product(session=SessionDep, user_id=user_id, favorite_product_id=product_id)
    return "success"

@router.get("user/favorite")
async def get_favorites(user_id: int):
    return await get_favorite_products_for_user(session=SessionDep, user_id=user_id)

@router.get("user")
async def get_user():
    ...
    
@router.get("user/role")
async def get_user_role():
    ...