import json

from typing import List
from sqlalchemy import delete, insert, update
from datetime import datetime

from app.posts.models import Post, Comment, Like
from app.database import async_session_maker
from app.services.base import BaseService


# Класс для работы с постами
class PostService(BaseService):
    model = Post

    # Создание поста с фотографиями
    @classmethod
    async def add_post_with_photos(cls, content: str, photos: List[str], owner_id: int):
        async with async_session_maker() as session:
            json_photos = json.dumps(photos)
            query = insert(cls.model).values(content=content, photos = json_photos, owner_id=owner_id)
            await session.execute(query)
            await session.commit()


    # Создание поста без фотографий
    @classmethod
    async def add_post(cls, content: str, owner_id: int):
        async with async_session_maker() as session:
            query = insert(cls.model).values(content=content, owner_id=owner_id)
            await session.execute(query)
            await session.commit()


    # Редактирование поста с фотографиями
    @classmethod
    async def edit_post_with_photos(cls, content: str, photos: List[str], post_id: int):
        async with async_session_maker() as session:
            json_photos = json.dumps(photos)
            query = update(cls.model).where(cls.model.id == post_id).values(content=content, photos=json_photos, date_last_updated=datetime.now())
            await session.execute(query)
            await session.commit()


    # Редактирование поста без фотографий
    @classmethod
    async def edit_post(cls, content: str, post_id: int):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == post_id).values(content=content, date_last_updated=datetime.now())
            await session.execute(query)
            await session.commit()
            

# Класс для работы с комментариями
class CommentService(BaseService):
    model = Comment


    # # Удаление комментариев, связанных с каким-то постом
    # @classmethod
    # async def delete_comments(cls, post_id: int):
    #     async with async_session_maker() as session:
    #         comments = delete(cls.model).where(cls.model.post_id == post_id)
    #         await session.execute(comments)
    #         await session.commit()


    # Редактирование комментария
    @classmethod
    async def edit_comment(cls, text: str, comment_id: int):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == comment_id).values(text=text, date_last_updated=datetime.now())
            await session.execute(query)
            await session.commit()


# Класс для работы с лайками
class LikeService(BaseService):
    model = Like

    # Обновление дизлайка
    @classmethod
    async def update_dislike(cls, dislike_id: int):
        async with async_session_maker() as session:
            like = update(cls.model).where(cls.model.id == dislike_id).values(degree=False)
            await session.execute(like)
            await session.commit()


    # Обновление лайка
    @classmethod
    async def update_like(cls, like_id: int):
        async with async_session_maker() as session:
            like = update(cls.model).where(cls.model.id == like_id).values(degree=True)
            await session.execute(like)
            await session.commit()


    # # Удаление комментариев, связанных с каким-то постом
    # @classmethod
    # async def delete_likes(cls, post_id: int):
    #     async with async_session_maker() as session:
    #         comments = delete(cls.model).where(cls.model.post_id == post_id)
    #         await session.execute(comments)
    #         await session.commit()

