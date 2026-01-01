from fastapi import FastAPI
from sqlmodel import Session, select
from database import engine
from models import Lyrics

app = FastAPI(title="Lyrics API")

@app.get("/")
def root():
    return {"status":"API is running"}

@app.post("/lyrics")
def add_song(lyrics: Lyrics):
    with Session(engine) as session:
        session.add(lyrics)
        session.commit()
        return lyrics
    
@app.get("/lyrics")
def get_all_songs():
    with Session(engine) as session:
        return session.exec(select(Lyrics)).all()
    
@app.get("/lyrics/{lyrics_id}")
def get_lyrics_id(lyrics_id: int):
    with Session(engine) as session:
        return session.get(Lyrics, lyrics_id)