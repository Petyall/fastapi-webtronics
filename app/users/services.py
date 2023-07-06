from sqlalchemy import update

from app.users.models import User
from app.database import async_session_maker
from app.services.base import BaseService

class UserService(BaseService):
    model = User

    # Обновление значений у пользователя
    @classmethod
    async def update_user(cls, email, **data):
        # Создание сессии для работы с БД
        async with async_session_maker() as session:
            table = cls.model
            query = update(table).where(table.email==email).values(**data)
            await session.execute(query)
            await session.commit()
