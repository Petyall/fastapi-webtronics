from sqladmin import ModelView

from app.users.models import User, Role
from app.posts.models import Like, Comment, Post


# Модель пользователей для админки
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"


# Модель Ролей для админки
class RoleAdmin(ModelView, model=Role):
    column_list = [Role.id, Role.name]
    name = "Роль"
    name_plural = "Роли"


# Модель Ролей для админки
class LikeAdmin(ModelView, model=Like):
    column_list = [Like.id, Like.degree]
    name = "Лайк"
    name_plural = "Лайки"


# Модель Ролей для админки
class CommentAdmin(ModelView, model=Comment):
    column_list = [column.name for column in Comment.__table__.columns]
    name = "Комментарий"
    name_plural = "Комментарии"


# Модель Ролей для админки
class PostAdmin(ModelView, model=Post):
    column_list = [column.name for column in Post.__table__.columns]
    name = "Пост"
    name_plural = "Посты"




