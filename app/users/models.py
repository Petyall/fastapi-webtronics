from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime

from app.database import Base


class User(Base):
    # Название таблицы
    __tablename__ = "users"

    # Поля
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(ForeignKey("roles.id"), default=1)
    uuid = Column(String())
    # uuid = Column(String, default=str(uuid4()))
    is_confirmed = Column(Boolean())
    confirmation_sent = Column(DateTime())
    confirmation_date = Column(DateTime())

    # Создание отношения для SQLAlchemy
    role = relationship("Role", back_populates="users")
    posts = relationship("Post", back_populates="owner")
    # comments = relationship("Comment", back_populates="owner")

    # Фукнция переопределяющая отображения названия модели
    def __str__(self):
        return f"Пользователь {self.email}"
    

class Role(Base):
    # Название таблицы
    __tablename__ = "roles"

    # Поля
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)

    # Создание отношения для SQLAlchemy
    users = relationship("User", back_populates="role")

    # Фукнция переопределяющая отображения названия модели
    def __str__(self):
        return f"{self.name}"
    