from fastapi import APIRouter, Query
from src.api.schemas.user import UserCreate
from src.db.repositories.user import (
    create_user, 
    add_favorite_product, 
    remove_favorite_product, 
    get_favorite_products_for_user
)
from src.dependencies import SessionDep

router = APIRouter()

# ✅ ИСПРАВЛЕНО: добавлен session_dep как параметр
@router.post("/user")
async def register_user(new_user: UserCreate, session_dep: SessionDep):
    user = await create_user(session=session_dep, new_user_schema=new_user)
    return {"status": "success", "user_id": user.id}

# ✅ ИСПРАВЛЕНО: добавлен session_dep и Query для параметров
@router.put("/user/favorite")
async def update_favorite_product(
    session_dep: SessionDep,
    user_id: int = Query(...),
    product_id: int = Query(...)
):
    await add_favorite_product(
        session=session_dep, 
        user_id=user_id, 
        favorite_product_id=product_id
    )
    return {"status": "success"}

# ✅ ИСПРАВЛЕНО: добавлен "/" в начале, session_dep, Query и await
@router.delete("/user/favorite")
async def delete_favorite_product(
    session_dep: SessionDep,
    user_id: int = Query(...),
    product_id: int = Query(...)
):
    await remove_favorite_product(
        session=session_dep, 
        user_id=user_id, 
        favorite_product_id=product_id
    )
    return {"status": "success"}

# ✅ ИСПРАВЛЕНО: добавлен "/" в начале, session_dep и Query
@router.get("/user/favorite")
async def get_favorites(
    session_dep: SessionDep,
    user_id: int = Query(...)
):
    return await get_favorite_products_for_user(
        session=session_dep, 
        user_id=user_id
    )

# ✅ ИСПРАВЛЕНО: добавлен "/" в начале
@router.get("/user")
async def get_user(session_dep: SessionDep, user_id: int = Query(...)):
    # TODO: реализовать получение пользователя
    pass
    
# ✅ ИСПРАВЛЕНО: добавлен "/" в начале
@router.get("/user/role")
async def get_user_role(session_dep: SessionDep, user_id: int = Query(...)):
    # TODO: реализовать получение роли пользователя
    pass
