from app.posts.services import PostService, CommentService
from app.exceptions import NotEnoughAuthorityException, PostNotFoundException, CommentNotFoundException


async def check_post(post_id, current_user):
    # Попытка получить пост
    post = await PostService.find_one_or_none(id=post_id)
    # Возврат ошибки, если пост не существует
    if not post:
        raise PostNotFoundException
    # Возврат ошибки, если автор поста не подошел
    if post.owner_id != current_user.id:
        raise NotEnoughAuthorityException
    

async def check_post_for_likes(post_id, current_user):
    # Попытка получить пост
    post = await PostService.find_one_or_none(id=post_id)
    # Возврат ошибки, если пост не существует
    if not post:
        raise PostNotFoundException
    # Возврат ошибки, если это автор поста
    if post.owner_id == current_user.id:
        raise NotEnoughAuthorityException


async def images_upload(photos):
    saved_photos = []
    # Перебор прикрепленных фотографий для их сохранения
    for photo in photos:
        contents = await photo.read()
        # Путь до фотографии
        save_path = f"app/static/images/{photo.filename}"
        # Сохранение фотографии
        with open(save_path, "wb") as f:
            f.write(contents)
        saved_photos.append(save_path)
    return saved_photos


async def check_comment(comment_id, post_id, current_user):
    # Попытка получить комментарий из БД
    comment = await CommentService.find_one_or_none(id=comment_id, post_id=post_id)
    # Возврат ошибки, если комментарий не найден
    if not comment:
        raise CommentNotFoundException
    # Возврат ошибки, если автор комментария не подошел 
    if comment.owner_id != current_user.id:
        raise NotEnoughAuthorityException
    # Возврат комментария
    return comment
