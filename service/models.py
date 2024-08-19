from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True)
    password = Column(String(256))
    created_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    ip = Column(String(50))

    # Bu ilişkiyi ekleyin
    comments = relationship("Comment", back_populates="user")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    ip = Column(String(50))
    comment_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    classifiedId = Column(String(50))

    # Bu ilişkiyi ekleyin
    user = relationship("User", back_populates="comments")
