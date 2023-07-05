from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from app.posts.models import Post, Comment, Like
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(ForeignKey("roles.id"), default=1)
    uuid = Column(String())
    is_confirmed = Column(Boolean())
    confirmation_sent = Column(DateTime())
    confirmation_date = Column(DateTime())

    role = relationship("Role", back_populates="users")
    posts = relationship("Post", back_populates="owner", foreign_keys=[Post.owner_id])
    comments = relationship("Comment", back_populates="owner", foreign_keys=[Comment.owner_id])
    likes = relationship("Like", back_populates="owner", foreign_keys=[Like.owner_id])

    def __str__(self):
        return f"Пользователь {self.email}"


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)

    users = relationship("User", back_populates="role")

    def __str__(self):
        return f"{self.name}"
    
    
# class User(Base):
#     # Название таблицы
#     __tablename__ = "users"

#     # Поля
#     id = Column(Integer, primary_key=True, nullable=False)
#     email = Column(String, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     role_id = Column(ForeignKey("roles.id"), default=1)
#     uuid = Column(String())
#     # uuid = Column(String, default=str(uuid4()))
#     is_confirmed = Column(Boolean())
#     confirmation_sent = Column(DateTime())
#     confirmation_date = Column(DateTime())
#     posts_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
#     comments_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
#     likes_id = Column(Integer, ForeignKey("likes.id"), nullable=True)


#     # Создание отношения для SQLAlchemy
#     role = relationship("Role", back_populates="users")
#     posts = relationship("Post", back_populates="users")
#     comments = relationship("Comment", back_populates="users")
#     likes = relationship("Like", back_populates="users")

#     # Фукнция переопределяющая отображения названия модели
#     def __str__(self):
#         return f"Пользователь {self.email}"
    
    