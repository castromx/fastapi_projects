from fastapi import FastAPI
from users_item import auth_routes, item_routes

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(item_routes.router)