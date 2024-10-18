from fastapi import FastAPI

from database_config.database import create_db_and_tables
from users_item import auth_routes, item_routes

create_db_and_tables()

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(item_routes.router)