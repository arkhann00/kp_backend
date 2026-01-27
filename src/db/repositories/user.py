from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.api.schemas.user import UserCreate
from src.models.user import User
from src.db.repositories.products import get_products_by_ids


async def create_user(session: AsyncSession, new_user_schema: UserCreate):
    # ✅ Сначала проверяем - может пользователь уже есть?
    result = await session.execute(
        select(User).where(User.telegram_id == new_user_schema.telegram_id)
    )
    existing_user = result.scalar_one_or_none()
    
    # Если пользователь уже есть - возвращаем его
    if existing_user:
        return existing_user
    
    # Если нет - создаём нового
    new_user_model = User(
        telegram_id=new_user_schema.telegram_id,
        username=new_user_schema.username,
        first_name=new_user_schema.first_name,
        second_name=new_user_schema.second_name,
        image_url=new_user_schema.image_url
    )
    
    session.add(new_user_model)
    await session.commit()
    await session.refresh(new_user_model)
    return new_user_model


async def add_favorite_product(session: AsyncSession, user_id: int, favorite_product_id: int):
    user = await session.get(User, user_id)
    
    if not user:
        raise ValueError("User not found")
    
    # Проверяем что товар ещё не в избранном
    if favorite_product_id not in user.favorite_product_ids:
        user.favorite_product_ids.append(favorite_product_id)
        await session.commit()
        await session.refresh(user)
    
    return user


async def remove_favorite_product(session: AsyncSession, user_id: int, favorite_product_id: int):
    user = await session.get(User, user_id)
    
    if not user:
        raise ValueError("User not found")
    
    if favorite_product_id in user.favorite_product_ids:
        user.favorite_product_ids.remove(favorite_product_id)
        await session.commit()
        await session.refresh(user)
    
    return user


async def get_favorite_products_for_user(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    
    if not user:
        return []
    
    favorite_products_ids = user.favorite_product_ids
    
    if not favorite_products_ids:
        return []
    
    return await get_products_by_ids(session, favorite_products_ids)
