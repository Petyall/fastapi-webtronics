from typing import List
from sqlalchemy import delete, select, insert, update
from datetime import datetime
from app.posts.models import Post, Comment, Like
from app.database import async_session_maker
import json
from app.services.base import BaseService


class PostService(BaseService):
    model = Post

    @classmethod
    async def add_post_with_photos(cls, content: str, photos: List[str], owner_id: int):
        async with async_session_maker() as session:
            json_photos = json.dumps(photos)
            query = insert(cls.model).values(content=content, photos = json_photos, owner_id=owner_id)
            # query = insert(cls.model).values(content=content, photos = [photo for photo in photos])
            await session.execute(query)
            await session.commit()

    @classmethod
    async def add_post(cls, content: str, owner_id: int):
        async with async_session_maker() as session:
            query = insert(cls.model).values(content=content, owner_id=owner_id)
            # query = insert(cls.model).values(content=content, photos = [photo for photo in photos])
            await session.execute(query)
            await session.commit()

    @classmethod
    async def edit_post_with_photos(cls, content: str, photos: List[str], post_id: int):
        async with async_session_maker() as session:
            json_photos = json.dumps(photos)
            query = update(cls.model).where(cls.model.id == post_id).values(content=content, photos=json_photos, date_last_updated=datetime.now())
            await session.execute(query)
            await session.commit()

    @classmethod
    async def edit_post(cls, content: str, post_id: int):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == post_id).values(content=content, date_last_updated=datetime.now())
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_post(cls, post_id: int):
        async with async_session_maker() as session:
            post = delete(cls.model).where(cls.model.id == post_id)
            await session.execute(post)
            await session.commit()
            

class CommentService(BaseService):
    model = Comment

    @classmethod
    async def add_comment(cls, text: str, post_id: int, owner_id: int):
        async with async_session_maker() as session:
            query = insert(cls.model).values(text=text, post_id=post_id, owner_id=owner_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_comments(cls, post_id: int):
        async with async_session_maker() as session:
            comments = delete(cls.model).where(cls.model.post_id == post_id)
            await session.execute(comments)
            await session.commit()

    @classmethod
    async def edit_comment(cls, text: str, comment_id: int):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == comment_id).values(text=text, date_last_updated=datetime.now())
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_comment(cls, comment_id: int):
        async with async_session_maker() as session:
            comments = delete(cls.model).where(cls.model.id == comment_id)
            await session.execute(comments)
            await session.commit()


class LikeService(BaseService):
    model = Like

    @classmethod
    async def delete_like(cls, like_id: int):
        async with async_session_maker() as session:
            like = delete(cls.model).where(cls.model.id == like_id)
            await session.execute(like)
            await session.commit()

    @classmethod
    async def update_dislike(cls, dislike_id: int):
        async with async_session_maker() as session:
            like = update(cls.model).where(cls.model.id == dislike_id).values(degree=False)
            await session.execute(like)
            await session.commit()

    @classmethod
    async def update_like(cls, like_id: int):
        async with async_session_maker() as session:
            like = update(cls.model).where(cls.model.id == like_id).values(degree=True)
            await session.execute(like)
            await session.commit()



