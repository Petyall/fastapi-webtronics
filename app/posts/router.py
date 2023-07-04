from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi import UploadFile, APIRouter
from typing import List, Optional
from app.posts.services import PostService, CommentService
from app.users.dependences import get_current_user
from app.users.models import User
from app.posts.schemas import PostWithComments

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


@router.get("/post_with_comments/{post_id}")
async def get_post_with_comments(post_id: int):
    post = await PostService.find_one_or_none(id=post_id)
    if post:
        comments = await CommentService.find_all(post_id = post_id)
        post_with_comments = PostWithComments(post=post, comments=comments)
        return post_with_comments
    


@router.post("/comment")
async def add_comment(text: str, post_id: int, current_user: User = Depends(get_current_user)):
    post = await PostService.find_one_or_none(id=post_id)
    if post:
        await CommentService.add_comment(text=text, post_id=post_id, owner_id=current_user.id)

@router.put("/comment")
async def edit_comment(post_id: int, comment_id, text: str, current_user: User = Depends(get_current_user)):
    comment = await CommentService.find_one_or_none(id=comment_id, post_id=post_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if comment.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Данный пост не ваш")
        
    await CommentService.edit_comment(text=text, comment_id=comment_id)

    return {"message": "Комментарий успешно изменен"}


@router.delete("/comment")
async def delete_comment(comment_id: int, current_user: User = Depends(get_current_user)):
    comment = await CommentService.find_one_or_none(id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Post not found")
    if comment.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this post")
    
    await CommentService.delete_comment(comment_id=comment_id)
    
    return {"message": "Post deleted successfully"}


@router.put("/posts/{post_id}")
async def edit_post(post_id: int, content: str, photos: Optional[List[UploadFile]] = File(None), current_user: User = Depends(get_current_user)):
    post = await PostService.find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Данный пост не ваш")
    
    if photos:
        saved_photos = []
        for photo in photos:
            contents = await photo.read()
            save_path = f"app/static/images/{photo.filename}"
            with open(save_path, "wb") as f:
                f.write(contents)
            saved_photos.append(save_path)
        
        await PostService.edit_post_with_photos(post_id=post_id, content=content, photos=saved_photos)
    else:
        await PostService.edit_post(post=post, content=content)

    return {"message": "Пост успешно изменен"}


@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, current_user: User = Depends(get_current_user)):
    post = await PostService.find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this post")
    
    await PostService.delete_post(post_id=post_id)
    await CommentService.delete_comments(post_id=post_id)
    
    return {"message": "Post deleted successfully"}