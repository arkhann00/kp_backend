from fastapi import APIRouter, Query
from pydantic import BaseModel
from src.api.schemas.user import UserCreate
from src.db.repositories.user import (
    create_user, 
    add_favorite_product, 
    remove_favorite_product, 
    get_favorite_products_for_user
)
from src.dependencies import SessionDep

router = APIRouter()

class FavoriteRequest(BaseModel):
    user_id: str  # ✅ Теперь это telegram_id (строка)
    product_id: int

@router.post("/user")
async def register_user(new_user: UserCreate, session_dep: SessionDep):
    user = await create_user(session=session_dep, new_user_schema=new_user)
    return {"status": "success", "user_id": user.telegram_id}  # ✅ Возвращаем telegram_id

# ✅ Принимаем telegram_id как строку
@router.put("/user/favorite")
async def update_favorite_product(
    favorite: FavoriteRequest,
    session_dep: SessionDep
):
    await add_favorite_product(
        session=session_dep, 
        telegram_id=favorite.user_id,  # ✅ Передаём telegram_id
        favorite_product_id=favorite.product_id
    )
    return {"status": "success"}

@router.delete("/user/favorite")
async def delete_favorite_product(
    favorite: FavoriteRequest,
    session_dep: SessionDep
):
    await remove_favorite_product(
        session=session_dep, 
        telegram_id=favorite.user_id,  # ✅ Передаём telegram_id
        favorite_product_id=favorite.product_id
    )
    return {"status": "success"}

# ✅ Принимаем telegram_id через Query
@router.get("/user/favorite")
async def get_favorites(
    session_dep: SessionDep,
    user_id: str = Query(...)  # ✅ Теперь строка
):
    return await get_favorite_products_for_user(
        session=session_dep, 
        telegram_id=user_id
    )
