import requests
import json
import os
from app.services.utils import generate_embedding

def fetch_books_from_google(keyword, max_results=40):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": keyword,
        "maxResults": max_results
    }
    response = requests.get(url, params=params)
    items = response.json().get("items", [])
    print(f"Fetched {len(items)} books for keyword: {keyword}")
    books = []

    for item in items:
        if items:
            info = item["volumeInfo"]
            book = {
                "title": info.get("title"),
                "author": ", ".join(info.get("authors", [])),
                "description": info.get("description", ""),
                "thumbnail": info.get("imageLinks", {}).get("thumbnail", ""),
                "previewLink": info.get("previewLink", ""),
                "maturityRating": info.get("maturityRating", ""),
                "categories": info.get("categories", []),
        }
        books.append(book)
    return books if books else None



def seed_books(keywords, output_path="app/data/book_embeddings.json"):
    all_books = []

    for keyword in keywords:
        print(f"Fetching books for: {keyword}")
        books = fetch_books_from_google(keyword)
        for book in books:
            if book["title"] in [b["title"] for b in all_books] and book["author"] in [b["author"] for b in all_books]:
                print(f"Skipping duplicate book: {book['title']}")
                continue
            embedding = generate_embedding((book["description"] if book["description"] else " " + book["title"]))
            if embedding:
                book["embedding"] = embedding
                all_books.append(book)

    # Save to JSON
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(all_books, f, indent=2)
    print(f"✅ Seeded {len(all_books)} books to {output_path}")

if __name__ == "__main__":
    seed_books([
        "Fiction",
        "Non-Fiction",
        "Science Fiction & Fantasy",
        "Romance",
        "Mystery & Thriller",
        "Young Adult (YA)",
        "Children’s Books",
        "Biographies & Memoirs",
        "Self-Help",
        "Health & Wellness",
        "History",
        "Psychology",
        "Business & Economics",
        "Religion & Spirituality",
        "Philosophy",
        "Education & Learning",
        "Technology & Computer Science",
        "Art & Photography",
        "Poetry",
        "Travel & Adventure",
        "Parenting & Relationships",
        "Politics & Social Sciences",
        "Cooking & Food",
        "Comics & Graphic Novels",
        "True Crime",
        "Horror",
        "Sports & Outdoors"
    ])
