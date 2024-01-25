from pydantic import BaseModel, EmailStr
# pydantic схеми для валідації данних в запитах

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class ItemBase(BaseModel):
    title: str
    description: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True