from sqlmodel import SQLModel, Field, create_engine, Session, select
from pathlib import Path
from typing import Optional
import re

class Lyrics(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    lyrics: str


DATABASE_URL = "sqlite://lyrics.db"
engine = create_engine(DATABASE_URL, echo=False)

def create_database():
    SQLModel.metadata.create_all(engine)