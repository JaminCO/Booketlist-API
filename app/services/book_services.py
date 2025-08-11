import requests
from app.models.models import SavedBook
from app.models.schema import SaveBookRequest
from sqlalchemy.orm import Session
from fastapi import Depends

def fetch_book_details(title: str) -> dict:
    """
    Fetch book details from an Google Books API using the title.
    
    Args:
        title (str): The title of the book to fetch details for.
    
    Returns:
        dict: A dictionary containing book details.
    """
    response = requests.get(
        "https://www.googleapis.com/books/v1/volumes",
        params={"q": title, "maxResults": 1}
    )
    items = response.json().get("items")

    if response.status_code == 200 and items:
        info = items[0]["volumeInfo"]
        return {
            "title": info.get("title"),
            "author": ", ".join(info.get("authors", [])),
            "description": info.get("description", ""),
            "thumbnail": info.get("imageLinks", {}).get("thumbnail", ""),
            "previewLink": info.get("previewLink", ""),
            "maturityRating": info.get("maturityRating", ""),
            "categories": info.get("categories", []),
        }
    else:
        return None

def save_book(book: SaveBookRequest, db: Session):
    saved_book = SavedBook(**book.dict())
    db.add(saved_book)
    db.commit()
    db.refresh(saved_book)
    return saved_book.id

def delete_book(book_id: int, user_id: int, db: Session):
    book = db.query(SavedBook).filter(SavedBook.id == book_id, SavedBook.user_id == user_id).first()
    if book:
        db.delete(book)
        db.commit()
        return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}