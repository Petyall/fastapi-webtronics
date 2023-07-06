from fastapi import APIRouter, Depends, Response
from datetime import datetime
from uuid import uuid4

from app.posts.services import PostService, LikeService, CommentService
from app.users.dependences import get_current_user
from app.users.models import User
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.services import UserService
from app.users.schemas import UserCreate, UserUpdate, UserLogin
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException, NotEnoughAuthorityException
from app.email import test_send_email_confirmation_email


router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и пользователи"],
)


@router.post("/register")
async def register_user(user_data: UserCreate):
    """
    Регистрация пользователя
    """
    # Проверка существования пользователя
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    # Возврат ошибки, если такой пользователь уже зарегистрирован
    if existing_user:
        raise UserAlreadyExistsException
    # Преобразование пароля в хэшированный
    hashed_password = get_password_hash(user_data.password)
    # Создание пользователя
    await UserService.add(email=user_data.email, first_name=user_data.first_name, last_name=user_data.last_name, hashed_password=hashed_password, uuid=str(uuid4()), is_confirmed=False)
    # Отправка ссылки подтверждения пользователю
    confirmation_link = await test_send_email_confirmation_email(user_data.email)
    # Добавление даты отправки ссылки подтверждения в БД
    await UserService.update_user(email=user_data.email, confirmation_sent=datetime.now())
    # Возврат успешного сообщения
    # return f"Для подтверждения пользователя {user_data.email} было отправлено письмо с ссылкой для завершения регистрации"
    return f"Для подтверждения пользователя {user_data.email} должно было быть отправлено письмо, но в режиме тестирования, оно не отправилось. Вы можете перейти по ссылке {confirmation_link}"


@router.get("/confirm-email")
async def confirm_email(email: str, uuid: str):
    """
    Подтверждение электронной почты
    """
    # Получение пользователя из БД
    user = await UserService.find_one_or_none(uuid=uuid)
    # Возврат ошибки, если пользователь не найден
    if not user:
        return {"message": "Пользователь не найден."}
    # Возврат ошибки, если пользователь уже подтвержден
    if user.is_confirmed:
        return {"message": "Пользователь уже подтвержден."}
    # Сохранение статуса подтверждения пользователя в БД
    user = await UserService.update_user(email=email, is_confirmed=True, confirmation_date=datetime.now())
    # Возврат успешного сообщения
    return {"message": "Электронный адрес подтвержден."}


@router.post("/login")
async def login_user(response: Response, user_data: UserLogin):
    """
    Авторизация пользователя
    """
    # Попытка авторизации пользователя
    user = await authenticate_user(user_data.email, user_data.password)
    # Возврат ошибки, если пользователь не зарегистрирован или не подошел пароль
    if not user:
        raise IncorrectEmailOrPasswordException
    # Создание и передача токена в cookie 
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True
    )
    # Возврат успешного сообщения
    return f"Пользователь {user_data.email} успешно авторизован"


@router.post("/logout")
async def logout_user(response: Response):
    """
    Выход пользователя
    """
    # Удаление токена из cookie
    response.delete_cookie("access_token")
    return "До свидания!"


@router.put("/profile")
async def update_user(user_data: UserUpdate, current_user: User = Depends(get_current_user)):
    """
    Обновление информации о пользователе
    """
    await UserService.update_user(email=current_user.email, first_name=user_data.first_name, last_name=user_data.last_name)


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Получение информации о пользователе
    """
    return(current_user)


@router.get("/all")
async def read_users_all(current_user: User = Depends(get_current_user)):
    """
    Получение информации обо всех пользователях
    """
    # Проверка роли пользователя
    if current_user.role_id == 2:
        # Возврат списка пользователей
        return await UserService.find_all()
    # Возврат ошибки, если пользователь не админ
    else:
        raise NotEnoughAuthorityException


@router.get("/id/{user_id}")
async def read_users_id(user_id: int, current_user: User = Depends(get_current_user)):
    """
    Получение информации о пользователе по id
    """
    # Проверка роли пользователя
    if current_user.role_id == 2:
        # Возврат конкретного пользователя
        return await UserService.find_one_or_none(id=user_id)
    # Возврат ошибки, если пользователь не админ
    else:
        raise NotEnoughAuthorityException
    

@router.get("/profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Получение личного кабинета пользователя
    """
    context = {
        "user": current_user,
        "posts": await PostService.find_all(owner_id=current_user.id),
        "comments": await CommentService.find_all(owner_id=current_user.id),
        "likes": await LikeService.find_all(owner_id=current_user.id)
    }
    return(context)