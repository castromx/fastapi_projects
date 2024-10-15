from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
import models, schemas, crud, database
from sqlalchemy.ext.asyncio import AsyncSession


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login/",
)

def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    db: AsyncSession = Depends(database.get_async_session),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    user = db.query(models.UserModel).filter(models.UserModel.username == username).first()
    if not user or not crud.validate_password(password=password, hashed_password=user.password):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User inactive",
        )
    return user


def register_user(
    user_data: schemas.UserSchema, db: AsyncSession):
    existing_user = db.query(models.UserModel).filter(models.UserModel.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = crud.hash_password(user_data.password)
    new_user = models.UserModel(username=user_data.username, password=hashed_password, email=user_data.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    jwt_payload = {
        "sub": new_user.username,
        "username": new_user.username,
        "email": new_user.email,
    }
    token = crud.encode_jwt(jwt_payload)
    return schemas.TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = crud.auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}",
        )
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload), db: AsyncSession = Depends(database.get_async_session)
) -> models.UserModel:
    username: str | None = payload.get("sub")
    user = db.query(models.UserModel).filter(models.UserModel.username == username).first()
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid (user not found)",
    )


def get_current_active_auth_user(
    user: models.UserModel = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive",
    )