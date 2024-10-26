from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.util import await_only

from database.crud import get_current_auth_user
from database.models import ItemModel, UserModel
from database.schemas import ItemCreate, Item
from database.database import get_async_session

router = APIRouter(tags=['items'])




@router.post("/items", response_model=Item)
async def create_item(
    item: ItemCreate, db: AsyncSession = Depends(get_async_session), current_user: UserModel = Depends(get_current_auth_user)):
    new_item = ItemModel(**item.dict(), owner_id=current_user.id)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(ItemModel).filter(ItemModel.id == item_id))
    item = result.scalar_one_or_none()
    if item:
        return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found",
    )


@router.get("/items", response_model=list[Item])
async def read_user_items(
    current_user: UserModel = Depends(get_current_auth_user),
    db: AsyncSession = Depends(get_async_session),
):
    result = await db.execute(select(ItemModel).filter(ItemModel.owner_id == current_user.id))
    items = result.scalars().all()
    return items

