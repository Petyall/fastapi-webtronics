from typing import List
from sqlalchemy import select, insert, update

from app.posts.models import Post
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