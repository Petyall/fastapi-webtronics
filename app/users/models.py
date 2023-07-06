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
    