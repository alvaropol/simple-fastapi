from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQL_DATABASE_URL = 'sqlite:///./bookapi.db'

engine = create_engine(SQL_DATABASE_URL, connect_args={'check_same_thread': False})

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session() -> Session:
    session = Session()
    try:
        yield session
    finally:
        session.close()
