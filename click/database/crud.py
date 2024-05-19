from sqlalchemy.orm import Session
from datetime import datetime
from . import schemas, models
from typing import List


def create_user(db: Session, user: schemas.UserAccount):
    time_now = datetime.utcnow()
    user_data = user.dict(exclude={"register_at", "last_login_at"})
    db_user = models.User(**user_data, register_at=time_now, last_login_at=time_now)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user_score(db: Session, user_id: int):
    user = get_user(db, user_id)
    user_id = user.id
    scores = models.UserScore(user_id=user_id, score=0)
    db.add(scores)
    db.commit()
    db.refresh(scores)
    return scores


def get_user_scores(db: Session, user_id: int):
    return db.query(models.UserScore).filter(models.UserScore.user_id == user_id).first()


def add_point(db: Session, count: int, user_id: int):
    user = get_user(db, user_id)
    user_id = user.id
    score_user = get_user_scores(db, user_id)
    score_user.score += count
    db.add(score_user)
    db.commit()
    db.refresh(score_user)
    return score_user


def create_user_boost(db: Session, user_id: int):
    user = get_user(db, user_id)
    user_id = user.id
    boosts = models.Boosts(user_id=user_id, fill_char_count=1, charge_count=1, mine_coint=1)
    db.add(boosts)
    db.commit()
    db.refresh(boosts)
    return boosts


def get_user_boosts(db: Session, user_id: int):
    return db.query(models.Boosts).filter(models.Boosts.user_id == user_id).first()

def dev_charge(db: Session, user_id: int):
    boosts = get_user_boosts(db, user_id)
    count_miner = boosts.mine_coint
    boosts.charge_count -= count_miner
    db.commit()
    return boosts.charge_count
