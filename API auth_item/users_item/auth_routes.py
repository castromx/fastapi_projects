from fastapi import APIRouter, Depends
from database_config.schemas import TokenInfo
from database_config.models import Base, UserModel
from database_config.database import engine
from database_config import utils





router = APIRouter(tags=['auth']) 


Base.metadata.create_all(bind=engine)


@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserModel = Depends(utils.validate_auth_user),
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.post("/register", response_model=TokenInfo)
def register_user_and_issue_jwt(
    user: UserModel = Depends(utils.register_user),
):
    return user


@router.get("/users/me")
def auth_user_check_self_info(
    payload: dict = Depends(utils.get_current_token_payload),
    user: UserModel = Depends(utils.get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
