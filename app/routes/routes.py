from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from app.models.schema import RecommendationRequest, RecommendationResponse, RecommendedBook, SignupRequest, SaveBookRequest, SaveBookResponse, DeleteBookResponse, SavedBooksResponse
from app.services.book_services import fetch_book_details, save_book, delete_book
from app.services.utils import generate_embedding
from app.services.recommender import recommend_books
from app.services.user_services import create_user, get_current_user_dep, login_user
from app.models.models import User, SavedBook
from app.models.database import SessionLocal

load_dotenv()

router = APIRouter()

def get_db():
    try:
        # Create a new session
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    except Exception as e:
        print(f"DATABASE_CONNECTION_ERROR: {str(e)} - get_db")
        raise Exception("Database connection error")

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    user = User(
        username=request.username,
        email=request.email,
        password_hash=request.password
    )
    return create_user(user, db=db)

@router.post("/login")
def login(request: SignupRequest, db: Session = Depends(get_db)):
    return login_user(request.email, request.password, db=db)

@router.get("/user")
def get_user(current_user: User = Depends(get_current_user_dep)):
    return {"user": current_user}

@router.get("/saved_books")
def get_saved_books(current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    return {"saved_books": SavedBooksResponse(saved_books=current_user.saved_books), "length": len(current_user.saved_books)}

@router.post("/add_book", response_model=SaveBookResponse)
def add_book(request: SaveBookRequest, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    request.user_id = current_user.id
    book_id = save_book(request, db=db)
    return {"message": "Book added successfully.", "book_id": book_id}

@router.delete("/delete_book/{book_id}", response_model=DeleteBookResponse)
def delete_book(book_id: int, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    return delete_book(book_id, current_user.id, db=db)

@router.get("/books/{book_id}")
def get_book(book_id: int):
    return {"message": f"Details for book with ID {book_id} are not implemented yet."}

@router.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):
    books = request.books
    combined_description = ""
    for book in books:
        info = fetch_book_details(book)
        if info and info["description"]:
            combined_description += (info["description"] if info["description"] else " " + info["title"]) + " "

    if not combined_description:
        return {"recommendations": []}

    user_embedding = generate_embedding(combined_description)
    results = recommend_books(user_embedding)

    return {
        "recommendations": [RecommendedBook(**res) for res in results]
    }
