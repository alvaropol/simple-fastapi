from http.client import HTTPException
from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from book import Book
from dto.book_dto import BookDto
from database import get_session
from dto.get_book_dto import GetBookDto

app = FastAPI()


@app.get("/books", response_model=List[GetBookDto], status_code=HTTP_200_OK)
def get_all_books(db: Session = Depends(get_session)):
    books = db.query(Book).all()
    return {"books": [GetBookDto.from_orm(book) for book in books]}


@app.get("/books/{book_id}", response_model=GetBookDto, status_code=HTTP_200_OK)
def get_book(book_id: int, db: Session = Depends(get_session)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return GetBookDto.from_orm(db_book)


@app.post("/books/create", response_model=GetBookDto, status_code=HTTP_201_CREATED)
def create_book(dto: BookDto, db: Session = Depends(get_session)) -> GetBookDto:
    new_book = Book(title=dto.title, autor=dto.author, year=dto.year)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return GetBookDto.from_orm(new_book)


@app.put("/books/{book_id}", response_model=GetBookDto)
def update_book(book_id: int, book_edit: BookDto, db: Session = Depends(get_session)):
    book_found = db.query(Book).filter(Book.id == book_id).first()

    if book_found is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book_found.title = book_edit.title
    book_found.publication_date = book_edit.publication_date
    book_found.tags = book_edit.tags
    db.commit()
    db.refresh(book_found)
    return GetBookDto.from_orm(book_found)


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_session)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()