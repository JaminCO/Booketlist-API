from pydantic import BaseModel
from typing import List

# class BookInput(BaseModel):
#     title: str

class RecommendationRequest(BaseModel):
    books: List[str]

class RecommendedBook(BaseModel):
    title: str
    author: str
    reason: str
    summary: str
    categories: List[str]
    thumbnail: str
    previewLink: str
    maturityRating: str

class RecommendationResponse(BaseModel):
    recommendations: List[RecommendedBook]

class UserSchema(BaseModel):
    id: int
    username: str
    email: str

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class SaveBookRequest(BaseModel):
    book_title: str
    book_author: str
    book_description: str
    book_thumbnail: str
    book_preview_link: str
    book_maturity_rating: str
    book_categories: List[str]

class SaveBookResponse(BaseModel):
    message: str
    book_id: int

class DeleteBookResponse(BaseModel):
    message: str

class SavedBookSchema(BaseModel):
    id: int
    user_id: int
    book_title: str
    book_author: str
    book_description: str
    book_thumbnail: str
    book_preview_link: str
    book_maturity_rating: str
    book_categories: List[str]

class SavedBooksResponse(BaseModel):
    saved_books: List[SavedBookSchema]