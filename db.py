from sqlmodel import SQLModel, Field, create_engine, Session, select
from pathlib import Path
from typing import Optional
import re

class Lyrics(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)  # Index for faster searching
    artist: Optional[str] = Field(default=None, index=True)
    lyrics: str
    filename: str  # Track source file

# Database setup
DATABASE_URL = "sqlite:///lyrics.db"
engine = create_engine(DATABASE_URL, echo=False)

def create_db():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)

def extract_metadata_from_filename(filename: str) -> tuple[str, Optional[str]]:
    """
    Extract title and artist from filename.
    Supports formats like:
    - "Artist - Song Title.txt"
    - "Song Title.txt"
    """
    name = Path(filename).stem
    
    # Try to split by common separators
    if " - " in name:
        parts = name.split(" - ", 1)
        return parts[1].strip(), parts[0].strip()  # title, artist
    elif "_" in name:
        parts = name.split("_", 1)
        return parts[1].strip(), parts[0].strip()
    else:
        return name.strip(), None

def extract_metadata_from_content(content: str) -> tuple[Optional[str], Optional[str], str]:
    """
    Extract title and artist from file content if present.
    Looks for patterns like:
    Title: Song Name
    Artist: Artist Name
    
    Returns: (title, artist, cleaned_lyrics)
    """
    lines = content.split('\n')
    title = None
    artist = None
    lyrics_start = 0
    
    # Check first few lines for metadata
    for i, line in enumerate(lines[:5]):
        line = line.strip()
        if line.lower().startswith('title:'):
            title = line.split(':', 1)[1].strip()
            lyrics_start = max(lyrics_start, i + 1)
        elif line.lower().startswith('artist:'):
            artist = line.split(':', 1)[1].strip()
            lyrics_start = max(lyrics_start, i + 1)
    
    # Get lyrics without metadata lines
    lyrics = '\n'.join(lines[lyrics_start:]).strip()
    
    return title, artist, lyrics

def import_lyrics_file(filepath: Path, session: Session) -> bool:
    """
    Import a single lyrics file into the database.
    Returns True if successful, False otherwise.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to extract metadata from content first
        title_content, artist_content, lyrics = extract_metadata_from_content(content)
        
        # Fall back to filename if not in content
        if not title_content:
            title_content, artist_content = extract_metadata_from_filename(filepath.name)
            lyrics = content
        
        # Create and add to database
        lyrics_entry = Lyrics(
            title=title_content or filepath.stem,
            artist=artist_content,
            lyrics=lyrics,
            filename=filepath.name
        )
        
        session.add(lyrics_entry)
        session.commit()
        print(f"✓ Imported: {title_content}")
        return True
        
    except Exception as e:
        print(f"✗ Error importing {filepath.name}: {e}")
        return False

def import_lyrics_directory(directory: str):
    """Import all .txt files from a directory"""
    lyrics_dir = Path(directory)
    
    if not lyrics_dir.exists():
        print(f"Directory not found: {directory}")
        return
    
    txt_files = list(lyrics_dir.glob("*.txt"))
    
    if not txt_files:
        print(f"No .txt files found in {directory}")
        return
    
    print(f"Found {len(txt_files)} files to import...")
    
    with Session(engine) as session:
        success_count = 0
        for filepath in txt_files:
            if import_lyrics_file(filepath, session):
                success_count += 1
    
    print(f"\nImported {success_count}/{len(txt_files)} files successfully")

def search_by_title(title: str, session: Session) -> list[Lyrics]:
    """Search for songs by title (case-insensitive, partial match)"""
    statement = select(Lyrics).where(Lyrics.title.contains(title))
    return session.exec(statement).all()

def search_by_artist(artist: str, session: Session) -> list[Lyrics]:
    """Search for songs by artist (case-insensitive, partial match)"""
    statement = select(Lyrics).where(Lyrics.artist.contains(artist))
    return session.exec(statement).all()

def get_lyrics_by_id(lyrics_id: int, session: Session) -> Optional[Lyrics]:
    """Get lyrics by ID"""
    return session.get(Lyrics, lyrics_id)

def list_all_songs(session: Session) -> list[Lyrics]:
    """List all songs in database"""
    statement = select(Lyrics)
    return session.exec(statement).all()

# Example usage
if __name__ == "__main__":
    # Create database
    create_db()
    
    # Import lyrics from directory
    import_lyrics_directory("C:\Users\User\Documents\Lyrics")  # Change to your directory path
    
    # Example searches
    with Session(engine) as session:
        # Search by title
        results = search_by_title("love", session)
        print(f"\nFound {len(results)} songs with 'love' in title:")
        for song in results[:5]:  # Show first 5
            print(f"  - {song.title}" + (f" by {song.artist}" if song.artist else ""))
        
        # Get specific song
        if results:
            song = results[0]
            print(f"\nLyrics for '{song.title}':")
            print(song.lyrics[:200] + "...")  # Show first 200 chars