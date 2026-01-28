from fastapi import APIRouter, File, UploadFile
from src.api.schemas.product import ProductSchema

from src.db.repositories.products import (create_product_db, get_products_db, update_image_url, remove_product)
from src.dependencies import SessionDep
from src.utils import save_product_image


router = APIRouter()

@router.get("/products")
async def get_products(session_dep: SessionDep):
    return await get_products_db(session=session_dep)
     
@router.post("/products")
async def create_product(session_dep: SessionDep, new_product:ProductSchema):
    return await create_product_db(session= session_dep,new_product=new_product)
    
@router.get("/products/{product_id}")
async def get_product(session: SessionDep):
    ...

@router.post("/products/{product_id}/image")
async def add_product_image(session: SessionDep, product_id:int,image_file:UploadFile = File(...)):
    image_url = await save_product_image(file=image_file)
    await update_image_url(session=session,product_id=product_id,image_url=image_url)
    return "SUCCESS"

@router.delete("/products/{product_id}")
async def delete_product(session: SessionDep, product_id: int):
    """Удалить товар по ID"""
    result = await remove_product(product_id=product_id, session=session)
    return {"message": "Product deleted successfully", "id": product_id}