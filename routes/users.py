from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn

user_router = APIRouter(
    tags=["User"]
)

users = {}


@user_router.post("/signup")
async def sign_new_user(data: User) -> dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким адресом электронной почты уже существует. Измените адрес электронной почты и попробуйте еще раз"
        )
    users[data.email] = data
    return {
        "message": "Пользователь успешно добавлен!"
    }


@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    if users == {}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Сначала необходимо создать пользователя"
        )
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    if user.password != users[user.email].password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неверный пароль"
        )
    return {
        "message": "Авторизация успешна"
    }
