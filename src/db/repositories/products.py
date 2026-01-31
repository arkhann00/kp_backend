import os
from fastapi import HTTPException
from sqlalchemy import select
from src.models.product import Product
from src.api.schemas.product import ProductSchema
from sqlalchemy.ext.asyncio import AsyncSession

async def get_products_db(session: AsyncSession) -> list[Product]:
    result = await session.execute(select(Product))
    
    products = result.scalars().all()
    
    return products

async def create_product_db(session: AsyncSession, new_product: ProductSchema):
    new_product_model = Product(
        title=new_product.title,
        description=new_product.description,
        price=new_product.price,
        discont=new_product.discont,
        category=new_product.category,
        ozon_url=new_product.ozon_url,
        wildberries_url=new_product.wildberries_url
    )
    
    session.add(new_product_model)
    await session.commit()
    await session.refresh(new_product_model)
    
    return new_product_model

async def get_product_by_id(session: AsyncSession, product_id: int):
    return await session.get(Product, product_id)

async def update_image_url(session: AsyncSession, product_id:int, image_url: str):
    product = await session.get(Product, product_id)
    
    product.image_url = image_url
    await session.commit()
    await session.refresh(product)
    
async def get_products_by_ids(session:AsyncSession, product_ids:list[int]):
    if not product_ids:
        return []
    result = await session.execute(
        select(Product).where(Product.id.in_(product_ids))
    )
    return result.scalars().all()

async def remove_product(product_id: int, session: AsyncSession):
    """Удаляет товар и его изображение"""
    
    # ✅ Получаем товар из БД
    result = await session.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    # ✅ Проверяем что товар существует
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # ✅ Удаляем файл изображения если он есть
    if product.image_url:
        try:
            # Получаем путь к файлу из URL
            # Например: "/uploads/products/image.jpg" -> "uploads/products/image.jpg"
            file_path = product.image_url.lstrip("/")
            
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"✅ Удалено изображение: {file_path}")
        except Exception as e:
            print(f"⚠️ Ошибка удаления изображения: {e}")
            # Продолжаем удаление товара даже если не удалось удалить файл
    
    # ✅ Удаляем товар из БД
    await session.delete(product)
    await session.commit()
    
    return {"status": "success", "deleted_id": product_id}


async def get_all_cotegories(session: AsyncSession):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    categories_set = set()
    for product in products:
        categories_set.add(product.category)
    return list(categories_set)