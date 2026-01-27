from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import SessionDep
from src.api.schemas.user import UserCreate
from src.models.user import User
from src.db.repositories.products import get_products_by_ids

async def create_user(session: AsyncSession, new_user_schema: UserCreate):
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


async def add_favorite_product(session: AsyncSession, favorite_product_id: int, user_id: int):
    user = await session.get(User, user_id)
    user.favorite_product_ids.append(favorite_product_id)
    await session.commit()
    await session.refresh(user)
    
async def remove_favorite_product(session: AsyncSession, product_id: int, user_id:int):
    user = await session.get(User, user_id)
    user.favorite_product_ids.remove(user_id)
    await session.commit()
    await session.refresh(user)
    
async def get_favorite_products_for_user(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    favorite_products_ids = user.favorite_product_ids
    return await get_products_by_ids(session, favorite_products_ids)