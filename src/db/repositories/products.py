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