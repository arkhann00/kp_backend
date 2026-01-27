from src.dependencies import SessionDep as Session
from src.models.base import Base
from src.db.session import engine
from src.models.product import Product
from src.models.user import User

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)