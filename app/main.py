from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.users.router import router as router_users
from app.posts.router import router as router_posts
from sqladmin import Admin
from app.database import engine
from app.admin.admin import authentication_backend
from app.admin.views import UserAdmin, RoleAdmin, CommentAdmin, LikeAdmin, PostAdmin


app = FastAPI()
admin = Admin(app, engine, authentication_backend=authentication_backend)

# Роутеры
app.include_router(router_users)
app.include_router(router_posts)

# Разрешенные источники
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Set-Cookie", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers"],
)


# Добавление моделей в админку
admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(CommentAdmin)
admin.add_view(LikeAdmin)
admin.add_view(PostAdmin)