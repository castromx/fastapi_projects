from datetime import datetime

from pydantic import BaseModel



class UserAccount(BaseModel):
    name: str
    tg_id: int
    register_at: datetime
    last_login_at: datetime

    class Config:
        orm_mode = True

class UserScores(BaseModel):
    score: int

    class Config:
        orm_mode = True

class Boosts(BaseModel):
    user_id: int
    fill_char_count: int
    charge_count: int
    mine_coint: int

    class Config:
        orm_mode = True

class MainPage(BaseModel):
    user: UserAccount
    user_scores: UserScores
    boosts: Boosts

    class Config:
        orm_mode = True
