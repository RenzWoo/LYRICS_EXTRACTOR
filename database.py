from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
import re

postgres_url = "postgresql://postgres:admin@localhost:5432/lyricsdb"
engine = create_engine(postgres_url)

class Lyrics(SQLModel, table=True):
    id: int = Field(primary_key=True)
    song: str
    lyrics: str

SQLModel.metadata.create_all(engine)