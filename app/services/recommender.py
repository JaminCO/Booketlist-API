import faiss
import numpy as np
import json

# Load static book dataset with embeddings
with open("app/data/book_embeddings.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

book_texts = [book["description"] for book in dataset]
book_titles = [book["title"] for book in dataset]
book_authors = [book["author"] for book in dataset]
thumbnails = [book["thumbnail"] for book in dataset]
previewLinks = [book["previewLink"] for book in dataset]
maturityRatings = [book["maturityRating"] for book in dataset]
categories = [book["categories"] for book in dataset]
book_embeddings = np.array([book["embedding"] for book in dataset]).astype("float32")

index = faiss.IndexFlatL2(len(book_embeddings[0]))
index.add(book_embeddings)

def recommend_books(user_embedding, top_k=5):
    D, I = index.search(np.array([user_embedding]).astype("float32"), top_k)
    results = []
    for idx in I[0]:
        results.append({
            "title": book_titles[idx],
            "author": book_authors[idx],
            "summary": book_texts[idx],
            "thumbnail": thumbnails[idx],
            "previewLink": previewLinks[idx],
            "maturityRating": maturityRatings[idx],
            "categories": categories[idx],
            "reason": "Similar writing style and themes"
        })
    return results
