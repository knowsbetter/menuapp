from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@db:5432/postgres'  # Docker database
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:breakme@localhost:5432/my_menu" # Local database

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
