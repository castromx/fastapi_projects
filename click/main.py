import aioredis
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from starlette.middleware.cors import CORSMiddleware

from database import schemas, models, crud
from sqlalchemy.orm import Session
from database.database import get_db_session

app = FastAPI()

@app.get("/")
async def root():
    return status.HTTP_200_OK


@app.post("/create_user")
async def create_user(user: schemas.UserAccount, db: Session = Depends(get_db_session)) -> schemas.UserAccount:
    user = crud.create_user(db=db, user=user)
    crud.create_user_score(db, user.id)
    crud.create_user_boost(db, user.id)
    return user


@app.get("/get_user")
@cache(expire=3600)
async def get_user(id: int, db: Session = Depends(get_db_session)) -> schemas.UserAccount:
    return crud.get_user(db, id)


@app.get("/get_user_score")
async def get_user_score(user_id: int, db: Session = Depends(get_db_session)):
    return crud.get_user_scores(db, user_id)


@app.post("/create_user_scores")
async def create_user_scores(user_id: int, db: Session = Depends(get_db_session)):
    return crud.create_user_score(db, user_id)


@app.post("/add_user_scores")
async def add_user_scores(user_id: int, count: int, db: Session = Depends(get_db_session)):
    boosts = crud.get_user_boosts(db, user_id)
    charge = boosts.charge_count * 600
    count = boosts.mine_coint * count
    if charge > 1:
        crud.add_point(db, count, user_id)
        crud.dev_charge(db, user_id)
        charge_after = boosts.charge_count
        count_after = crud.get_user_scores(db, user_id)
        return {"charge": charge_after, "count": count_after.score}
    elif charge < 1:
        return "Energy charge too low"


@app.post("/create_user_boosts")
async def create_user_boosts(user_id: int, db: Session = Depends(get_db_session)):
    return crud.create_user_boost(db, user_id)

@app.get("/get_user_boosts")
async def get_user_boosts(user_id: int, db: Session = Depends(get_db_session)):
    boosts = crud.get_user_boosts(db, user_id)
    return boosts

@app.on_event('startup')
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="/cache")