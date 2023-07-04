from fastapi import APIRouter, UploadFile, File, Depends
from fastapi import UploadFile, APIRouter
from typing import List, Optional
from app.posts.services import PostService
from app.users.dependences import get_current_user
from app.users.models import User

router = APIRouter(
    prefix="/posts",
    tags=["Публикации"],
)


# БАГ SWAGGER_UI - https://github.com/tiangolo/fastapi/issues/1949 !!!
@router.post("/posts")
async def add_post(content: str, photos: Optional[List[UploadFile]] = File(None), current_user: User = Depends(get_current_user)):
    if photos:
        saved_photos = []
        for photo in photos:
            print(photo)
            contents = await photo.read()
            save_path = f"app/static/images/{photo.filename}"
            with open(save_path, "wb") as f:
                f.write(contents)
            saved_photos.append(save_path)
        await PostService.add_post_with_photos(content=content, photos=saved_photos, owner_id=current_user.id)
    else:
        await PostService.add_post(content=content, owner_id=current_user.id)


@router.get("/posts/{post_id}")
async def get_post(post_id: int):
    return await PostService.find_one_or_none(id=post_id)
