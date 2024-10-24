from sqladmin import Admin
from fastapi import FastAPI
from database.database import engine
from routers import auth_routes, item_routes
from database.admin import UserAdmin, ItemAdmin


app = FastAPI()
admin = Admin(app, engine)

app.include_router(auth_routes.router)
app.include_router(item_routes.router)


admin.add_view(UserAdmin)
admin.add_view(ItemAdmin)


@app.get("/")
async def root():
    return {"status": "ok"}
