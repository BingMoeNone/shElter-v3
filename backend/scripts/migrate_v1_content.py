import os
import sys
from sqlalchemy.orm import Session

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.connection import SessionLocal
from src.models.metro import Station, Line, StationLineJunction
from src.models.music import Track, Artist

# Configuration
V1_ROOT_PATH = r"c:\BM_Program\shElter-v1\00_shElter"
V1_MUSIC_PATH = r"c:\BM_Program\shElter-v1\00_shElter\03_Echoom\music"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def migrate_metro(db: Session):
    print("Migrating Metro Map...")
    
    # 1. Create Lines
    lines_data = [
        {"name": "Line 1 (Knowledge)", "color": "#FF4444", "required_level": 1},
        {"name": "Line 2 (Soul)", "color": "#4444FF", "required_level": 1},
        {"name": "Line 3 (Echo)", "color": "#44FF44", "required_level": 1},
    ]
    
    lines_map = {}
    for l_data in lines_data:
        line = db.query(Line).filter(Line.name == l_data["name"]).first()
        if not line:
            line = Line(**l_data)
            db.add(line)
            db.flush() # Get ID
        lines_map[l_data["name"]] = line
        
    # 2. Create Stations (Hardcoded for v1 structure compatibility)
    stations_data = [
        {
            "name": "Cryptonomicon", 
            "path_key": "01_Cryptonomicon", 
            "description": "The repository of forbidden knowledge.",
            "lines": ["Line 1 (Knowledge)"]
        },
        {
            "name": "SoulLoom", 
            "path_key": "02_SoulLoom", 
            "description": "Where digital souls are woven.",
            "lines": ["Line 2 (Soul)"]
        },
        {
            "name": "Echoom", 
            "path_key": "03_Echoom", 
            "description": "The chamber of resonating sounds.",
            "lines": ["Line 3 (Echo)"]
        },
         {
            "name": "SilentEmbryo", 
            "path_key": "04_SilentEmbryo", 
            "description": "A quiet place of gestation.",
            "lines": ["Line 1 (Knowledge)", "Line 2 (Soul)"]
        }
    ]
    
    for i, s_data in enumerate(stations_data):
        station = db.query(Station).filter(Station.path_key == s_data["path_key"]).first()
        if not station:
            station = Station(
                name=s_data["name"],
                path_key=s_data["path_key"],
                description=s_data["description"],
                min_level=1,
                meta_data={"x": 100 + (i * 150), "y": 300} # Simple layout
            )
            db.add(station)
            db.flush()
            print(f"Created station: {station.name}")
            
            # Link lines
            for line_name in s_data["lines"]:
                line = lines_map[line_name]
                junction = StationLineJunction(
                    station_id=station.id,
                    line_id=line.id,
                    order_index=i
                )
                db.add(junction)
    
    db.commit()

def migrate_music(db: Session):
    print(f"Migrating Music from {V1_MUSIC_PATH}...")
    
    if not os.path.exists(V1_MUSIC_PATH):
        print("Music directory not found.")
        return

    # Create default artist
    default_artist = db.query(Artist).filter(Artist.name == "Unknown").first()
    if not default_artist:
        default_artist = Artist(name="Unknown", bio="The default artist for migrated tracks.")
        db.add(default_artist)
        db.flush()

    audio_extensions = ['.mp3', '.wav', '.ogg']
    
    count = 0
    for filename in os.listdir(V1_MUSIC_PATH):
        ext = os.path.splitext(filename)[1].lower()
        if ext in audio_extensions:
            # Found audio file
            file_url = f"/music/{filename}" # Relative URL for frontend
            title = os.path.splitext(filename)[0]
            
            # Check if exists
            existing = db.query(Track).filter(Track.file_url == file_url).first()
            if existing:
                continue
                
            track = Track(
                title=title,
                file_url=file_url,
                duration=0, # Need to extract metadata later
                order=count
            )
            track.artists.append(default_artist)
            
            db.add(track)
            count += 1
            print(f"Migrated track: {title}")
            
    db.commit()
    print(f"Migrated {count} tracks.")

if __name__ == "__main__":
    db = next(get_db())
    migrate_metro(db)
    migrate_music(db)
