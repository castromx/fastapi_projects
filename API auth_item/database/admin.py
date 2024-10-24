from . import models
from sqladmin import ModelView


class UserAdmin(ModelView, model=models.UserModel):
    column_list = [models.UserModel.username, models.UserModel.active]


class ItemAdmin(ModelView, model=models.ItemModel):
    column_list = [models.ItemModel.title, models.ItemModel.owner_id]
