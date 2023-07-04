from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    photos = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    date_created = Column(DateTime, default=datetime.utcnow)
    date_last_updated = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="posts")
    # comments = relationship("Comment", back_populates="post")


# class Comment(Base):
#     __tablename__ = "comments"

#     id = Column(Integer, primary_key=True, index=True)
#     text = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#     post_id = Column(Integer, ForeignKey("posts.id"))
#     date_created = Column(DateTime, default=datetime.utcnow)
#     date_last_updated = Column(DateTime, default=datetime.utcnow)

#     owner = relationship("User", back_populates="comments")
#     post = relationship("Post", back_populates="comments")