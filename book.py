from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    publication_date = Column(DateTime, nullable=True)

    class Config:
        from_attributes = True
