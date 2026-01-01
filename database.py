from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
import re

postgres_url = "postgresql://postgres:admin@localhost:5432/lyricsdb"
engine = create_engine(postgres_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)