import os
import sys
from fastapi.testclient import TestClient

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import app

client = TestClient(app)

def verify_metro():
    print("Verifying Metro API...")
    
    # Check lines
    response = client.get("/api/v1/metro/lines")
    if response.status_code != 200:
        print(f"FAILED: /metro/lines returned {response.status_code}")
        return False
    
    lines = response.json()
    print(f"Found {len(lines)} lines.")
    if len(lines) != 3:
        print("FAILED: Expected 3 lines.")
        return False
        
    # Check stations
    response = client.get("/api/v1/metro/stations")
    if response.status_code != 200:
        print(f"FAILED: /metro/stations returned {response.status_code}")
        return False
        
    stations = response.json()
    print(f"Found {len(stations)} stations.")
    if len(stations) != 4:
        print("FAILED: Expected 4 stations.")
        return False
        
    print("Metro API Verified.")
    return True

def verify_music():
    print("\nVerifying Music API...")
    
    # Check tracks
    response = client.get("/api/v1/music/tracks")
    if response.status_code != 200:
        print(f"FAILED: /music/tracks returned {response.status_code}")
        return False
        
    tracks = response.json()
    print(f"Found {len(tracks)} tracks.")
    if len(tracks) < 9: # At least 9 tracks were migrated
        print("FAILED: Expected at least 9 tracks.")
        return False
        
    print("Music API Verified.")
    return True

if __name__ == "__main__":
    metro_ok = verify_metro()
    music_ok = verify_music()
    
    if metro_ok and music_ok:
        print("\nSUCCESS: All integration APIs verified.")
        sys.exit(0)
    else:
        print("\nFAILURE: Some verifications failed.")
        sys.exit(1)
