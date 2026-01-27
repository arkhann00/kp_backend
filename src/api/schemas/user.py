from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    telegram_id: str 
    username: Optional[str]
    first_name: Optional[str]
    second_name: Optional[str]
    image_url: Optional[str]

