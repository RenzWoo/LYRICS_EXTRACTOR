from sqlmodel import SQLModel, Field
from typing import Optional

class Lyrics(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    song: str
    lyrics: str