from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]