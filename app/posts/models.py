from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base






class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    date_created = Column(DateTime, default=datetime.utcnow)
    date_last_updated = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    photos = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    date_created = Column(DateTime, default=datetime.utcnow)
    date_last_updated = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", foreign_keys=[Comment.post_id], cascade="all, delete")
    likes = relationship("Like", back_populates="post")
    
# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(Integer, primary_key=True, index=True)
#     content = Column(String)
#     photos = Column(String, nullable=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#     comments_id = Column(Integer, ForeignKey("comments.id"))
#     likes_id = Column(Integer, ForeignKey("likes.id"))
#     date_created = Column(DateTime, default=datetime.utcnow)
#     date_last_updated = Column(DateTime, default=datetime.utcnow)

#     owner = relationship("User", back_populates="posts")
#     comments = relationship("Comment", back_populates="post")
#     likes = relationship("Like", back_populates="post")


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


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    degree = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    date_created = Column(DateTime, default=datetime.utcnow)
    date_last_updated = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")