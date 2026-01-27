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

# ✅ Схема для body запроса
class FavoriteRequest(BaseModel):
    user_id: int
    product_id: int

@router.post("/user")
async def register_user(new_user: UserCreate, session_dep: SessionDep):
    user = await create_user(session=session_dep, new_user_schema=new_user)
    return {"status": "success", "user_id": user.id}

# ✅ ИСПРАВЛЕНО: принимаем данные из body
@router.put("/user/favorite")
async def update_favorite_product(
    favorite: FavoriteRequest,
    session_dep: SessionDep
):
    await add_favorite_product(
        session=session_dep, 
        user_id=favorite.user_id, 
        favorite_product_id=favorite.product_id
    )
    return {"status": "success"}

# ✅ ИСПРАВЛЕНО: принимаем данные из body
@router.delete("/user/favorite")
async def delete_favorite_product(
    favorite: FavoriteRequest,
    session_dep: SessionDep
):
    await remove_favorite_product(
        session=session_dep, 
        user_id=favorite.user_id, 
        favorite_product_id=favorite.product_id
    )
    return {"status": "success"}

# GET запрос - параметры в URL остаются
@router.get("/user/favorite")
async def get_favorites(
    session_dep: SessionDep,
    user_id: int = Query(...)
):
    return await get_favorite_products_for_user(
        session=session_dep, 
        user_id=user_id
    )
