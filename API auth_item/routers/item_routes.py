from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import crud
from database.models import UserModel
from database.schemas import ItemCreate, Item
from database.database import get_async_session

router = APIRouter(tags=['items'])


@router.post("/create_items", response_model=Item)
async def create_item(
    item: ItemCreate, db: AsyncSession = Depends(get_async_session), current_user: UserModel = Depends(crud.get_current_auth_user)):
    new_item = await crud.create_item(db=db, item=item, current_user=current_user)
    return new_item


@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int, db: AsyncSession = Depends(get_async_session)):
    item = await crud.get_item(db=db, item_id=item_id)
    if item:
        return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found",
    )


@router.get("/items", response_model=list[Item])
async def read_user_items(
    current_user: UserModel = Depends(crud.get_current_auth_user), db: AsyncSession = Depends(get_async_session)):
    items = await crud.get_user_items(db=db, current_user=current_user)
    return items
