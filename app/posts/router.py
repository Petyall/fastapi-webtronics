from fastapi import APIRouter, UploadFile, File, Depends
from fastapi import UploadFile, APIRouter
from typing import List, Optional

from app.posts.dependences import check_post, images_upload, check_comment, check_post_for_likes
from app.posts.services import PostService, CommentService, LikeService
from app.users.dependences import get_current_user
from app.users.models import User
from app.posts.schemas import PostWithComments
from app.exceptions import PostNotFoundException


router = APIRouter(
    prefix="/posts",
    tags=["Публикации"],
)


# БАГ SWAGGER_UI - https://github.com/tiangolo/fastapi/issues/1949 !!!
@router.post("/")
async def add_post(content: str, photos: Optional[List[UploadFile]] = File(None), current_user: User = Depends(get_current_user)):
    """
    Создание поста
    """
    # Проверка прикрепления фотографий
    if photos:
        saved_photos = await images_upload(photos)     
        # Создание поста   
        await PostService.add_post_with_photos(content=content, photos=saved_photos, owner_id=current_user.id)
        # Возврат сообщения об успешном создании
        return {"message": "Пост с фотографиями успешно создан"}
    # Если не было фотографий, сработает создание поста без фотографий
    else:
        await PostService.add_post(content=content, owner_id=current_user.id)
        # Возврат сообщения об успешном создании
        return {"message": "Пост успешно создан"}


@router.get("/{post_id}")
async def get_post(post_id: int):
    """
    Получение поста по id
    """
    # Возврат поста
    return await PostService.find_one_or_none(id=post_id)


@router.get("/post_with_comments/{post_id}")
async def get_post_with_comments_and_likes(post_id: int):
    """
    Получение поста по id с комментариями
    """
    # Попытка найти пост и вернуть его вместе с комментариями
    post = await PostService.find_one_or_none(id=post_id)
    # Вывод поста с комментариями, если он существует
    if post:
        comments = await CommentService.find_all(post_id = post_id)
        likes = await LikeService.find_all(post_id = post_id, degree = True)
        dislikes = await LikeService.find_all(post_id = post_id, degree = False)
        post_with_comments = PostWithComments(post=post, comments=comments, likes=len(likes), dislikes=len(dislikes))
        return post_with_comments
    # Вывод ошибки, если поста не существует
    else:
        raise PostNotFoundException
    

@router.put("/{post_id}")
async def edit_post(post_id: int, content: str, photos: Optional[List[UploadFile]] = File(None), current_user: User = Depends(get_current_user)):
    """
    Обновление поста
    """
    # Попытка получить пост
    post = await check_post(post_id=post_id, current_user=current_user)
    # Обновление фотографий, если они были прикрелпенны
    if photos:
        saved_photos = await images_upload(photos)   
        # Сохранение поста     
        await PostService.edit_post_with_photos(post_id=post_id, content=content, photos=saved_photos)
    # Сохранение поста без фотографий, если их не было
    else:
        await PostService.edit_post(post=post, content=content)
    # Возврат сообщения об успешном изменении
    return {"message": "Пост успешно изменен"}


@router.delete("/{post_id}")
async def delete_post(post_id: int, current_user: User = Depends(get_current_user)):
    """
    Удаление поста
    """
    # Проверка поста
    await check_post(post_id=post_id, current_user=current_user)
    # Удаление поста
    await PostService.delete(id=post_id)
    # Удаления комментария
    await CommentService.delete_for_post(id=post_id)
    # Удаление лайков
    await LikeService.delete_for_post(id=post_id)
    # Возврат сообщения об успешном удалении
    return {"message": "Пост успешно удален"}
    

@router.post("/comment")
async def add_comment(text: str, post_id: int, current_user: User = Depends(get_current_user)):
    """
    Создание комментария
    """
    # Попытка получить пост, к которому добавится комментарий
    post = await PostService.find_one_or_none(id=post_id)
    if post:
        # Создание комментария
        await CommentService.add(text=text, post_id=post_id, owner_id=current_user.id)
        # Возврат сообщения об успешном создании
        return {"message": "Комментарий успешно создан"}
    else:
        raise PostNotFoundException


@router.put("/comment")
async def edit_comment(post_id: int, comment_id, text: str, current_user: User = Depends(get_current_user)):
    """
    Обновление комментария
    """
    # Проверка существования комментария
    await check_comment(comment_id=comment_id, post_id=post_id, current_user=current_user)
    # Обновление комментария
    await CommentService.edit_comment(text=text, comment_id=comment_id)
    # Возврат сообщения об успешном изменении
    return {"message": "Комментарий успешно изменен"}


@router.delete("/comment")
async def delete_comment(comment_id: int, post_id: int, current_user: User = Depends(get_current_user)):
    """
    Удаление комментария
    """
    # Проверка существования комментария
    await check_comment(comment_id=comment_id, post_id=post_id, current_user=current_user)
    # Удаление комментария
    await CommentService.delete(id=comment_id)
    # Возврат сообщения об успешном изменении
    return {"message": "Комментарий успешно удален"}


@router.get("/{post_id}/like")
async def add_like(post_id: int, current_user: User = Depends(get_current_user)):
    """
    Добавление лайка
    """
    # Попытка получить пост
    await check_post_for_likes(post_id=post_id, current_user=current_user)
    # Создание лайка
    like = await LikeService.find_one_or_none(post_id=post_id, owner_id=current_user.id)
    # Проверка существования лайка
    if like:
        # Удаление лайка, если он уже существует
        if like.degree:
            await LikeService.delete(id=like.id)
            # Возврат сообщения об успешном удалении
            return {"message": "Лайк успешно удален"}
        # Смена дизлайка на лайк
        else:
            await LikeService.update_like(like_id=like.id)
            # Возврат сообщения об успешном изменении
            return {"message": "Лайк успешно изменен"}
    # Создание лайка, если его нет
    else:
        await LikeService.add(post_id=post_id, owner_id=current_user.id, degree=True)
        # Возврат сообщения об успешном усоздании
        return {"message": "Лайк успешно добавлен"}


@router.get("/{post_id}/dislikes")
async def add_dislike(post_id: int, current_user: User = Depends(get_current_user)):
    """
    Добавление дизлайка
    """
    # Попытка получить пост
    await check_post_for_likes(post_id=post_id, current_user=current_user)
    # Создание дизлайка
    dislike = await LikeService.find_one_or_none(post_id=post_id, owner_id=current_user.id)
    # Проверка существования дизлайка
    if dislike:
        # Смена дизлайка на лайк
        if dislike.degree:
            await LikeService.update_dislike(dislike_id=dislike.id)
            # Возврат сообщения об успешном изменении
            return {"message": "Дизлайк успешно изменен"}
        # Удаление дизлайка
        else:
            await LikeService.delete(id=dislike.id)
            # Возврат сообщения об успешном удалении
            return {"message": "Дизлайк успешно удален"}
    # Создание дизлайка
    else:
        await LikeService.add(post_id=post_id, owner_id=current_user.id, degree=False)
        # Возврат сообщения об успешном создании
        return {"message": "Дизлайк успешно добавлен"}
    