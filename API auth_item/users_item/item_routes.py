from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_config.utils import get_current_auth_user
from database_config.models import ItemModel, UserModel, Base
from database_config.schemas import ItemCreate, Item
from database_config.database import get_async_session, engine

router = APIRouter(tags=['items'])

Base.metadata.create_all(bind=engine)



@router.post("/items", response_model=Item)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_auth_user),
):
    new_item = ItemModel(**item.dict(), owner_id=current_user.id)
    print(new_item)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_async_session)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if item:
        return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found",
    )


@router.get("/items", response_model=list[Item])
def read_user_items(
    current_user: UserModel = Depends(get_current_auth_user),
    db: Session = Depends(get_async_session),
):
    items = db.query(ItemModel).filter(ItemModel.owner_id == current_user.id).all()
    return items
