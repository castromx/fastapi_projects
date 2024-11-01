from http.client import responses
from urllib import response

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from database.schemas import TokenInfo, UserSchema
from database.models import UserModel
from database import crud, utils


router = APIRouter(tags=['auth'])


@router.post("/login", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: UserModel = Depends(crud.validate_auth_user),
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
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
async def register_user_endpoint(
    user_data: UserSchema,
    db: AsyncSession = Depends(get_async_session)
):
    return await crud.register_user(user_data, db)


@router.get("/users/me")
async def auth_user_check_self_info(
    payload: dict = Depends(utils.get_current_token_payload),
    user: UserModel = Depends(crud.get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
