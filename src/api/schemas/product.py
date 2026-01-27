from pydantic import BaseModel, Field
from typing import Optional

class ProductSchema(BaseModel):
    title:str
    description:str
    price:int
    discont:int
    category:str
    ozon_url:str
    wildberries_url:str