from celery import Celery
from fastapi import APIRouter, BackgroundTasks

celery = Celery('tasks', broker='redis://localhost:6379/')

router = APIRouter(prefix='/tasks', tags=['tasks'])

@celery.task
def add_user_score(count_in_db_charge, charge):
    return count_in_db_charge + charge

@router.post('/add_user_charge')
async def add_user_charge(backgound_tasks: BackgroundTasks, count_in_db_charge, charge):
    backgound_tasks.add_task(add_user_score, count_in_db_charge, charge)