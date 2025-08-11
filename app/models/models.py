from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from app.models.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=False, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    saved_books = relationship("SavedBook", back_populates="user", cascade="all, delete-orphan")


class SavedBook(Base):
    __tablename__ = "saved_books"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_title = Column(String(255), nullable=False)
    book_author = Column(String(255))
    book_description = Column(String)
    book_thumbnail = Column(String)
    book_preview_link = Column(String)
    book_maturity_rating = Column(String)
    book_categories = Column(String)

    user = relationship("User", back_populates="saved_books")