from http.client import HTTPException
from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from book import Book
from dto.book_dto import BookDto
from database import get_session, Base, engine

app = FastAPI()


@app.on_event('startup')
def create_db():
    Base.metadata.create_all(bind=engine)


@app.get("/books", status_code=HTTP_200_OK)
def get_all_books(db: Session = Depends(get_session)) -> List[BookDto]:
    books: List[Book] = db.query(Book).all()
    if not books: raise HTTPException(status_code=404, detail="Books not found")
    return [BookDto.from_orm(book) for book in books]


@app.get("/books/{book_id}", status_code=HTTP_200_OK)
def get_book(book_id: int, db: Session = Depends(get_session)) -> BookDto:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookDto.from_orm(db_book)


@app.post("/books/create", status_code=HTTP_201_CREATED)
def create_book(dto: BookDto, db: Session = Depends(get_session)) -> BookDto:
    new_book = Book(title=dto.title, author=dto.author, publication_date=dto.publication_date)
    db.add(new_book)
    return BookDto.from_orm(new_book)


@app.put("/books/{book_id}")
def update_book(book_id: int, book_edit: BookDto, db: Session = Depends(get_session)) -> BookDto:
    book_found = db.query(Book).filter(Book.id == book_id).first()

    if book_found is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if book_edit.title is not None:
        book_found.title = book_edit.title
    if book_edit.publication_date is not None:
        book_found.publication_date = book_edit.publication_date
    if book_edit.author is not None:
        book_found.author = book_edit.author

    return BookDto.from_orm(book_found)


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_session)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    return {f'book with {book_id} deleted': True}
