import os
import sys
import glob
from datetime import datetime
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Add backend directory to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.connection import SessionLocal
from src.models.user import User

# Configuration
V1_SOULLOOM_PATH = r"c:\BM_Program\shElter-v1\00_shElter\02_SoulLoom"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def parse_identity_file(file_path):
    """
    Parses 00_identity.dat
    Format:
    鏁板瓧鍖栬韩鍚嶇О: WMY
    鎬ф牸搴曡壊: 鏌愮鍗拌瘉
    鍒涘缓鏃堕棿: 2026-02-10 08:01:03
    鏈€鍚庣櫥褰? 2026-02-10 08:01:20
    """
    data = {}
    try:
        # Try UTF-8 first
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Fallback to GBK
        with open(file_path, 'r', encoding='gbk') as f:
            lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("鏁板瓧鍖栬韩鍚嶇О:"):
            data['username'] = line.split(":", 1)[1].strip()
        elif line.startswith("鎬ф牸搴曡壊:"):
            data['password'] = line.split(":", 1)[1].strip()
        elif line.startswith("鍒涘缓鏃堕棿:"):
            time_str = line.split(":", 1)[1].strip()
            try:
                data['created_at'] = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                data['created_at'] = datetime.utcnow()
    
    return data

def parse_rank_file(file_path):
    """
    Parses 02_rank.dat
    Format:
    8
    """
    if not os.path.exists(file_path):
        return 1
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return int(content)
    except (UnicodeDecodeError, ValueError):
        return 1

def migrate_users():
    db = next(get_db())
    print(f"Scanning for users in {V1_SOULLOOM_PATH}...")
    
    # Get all subdirectories
    user_dirs = [d for d in os.listdir(V1_SOULLOOM_PATH) if os.path.isdir(os.path.join(V1_SOULLOOM_PATH, d))]
    
    migrated_count = 0
    skipped_count = 0
    
    for user_dir_name in user_dirs:
        user_path = os.path.join(V1_SOULLOOM_PATH, user_dir_name)
        identity_file = os.path.join(user_path, "00_identity.dat")
        rank_file = os.path.join(user_path, "02_rank.dat")
        
        if not os.path.exists(identity_file):
            print(f"Skipping {user_dir_name}: No identity file found.")
            continue
            
        try:
            user_data = parse_identity_file(identity_file)
            level = parse_rank_file(rank_file)
            
            username = user_data.get('username', user_dir_name)
            password = user_data.get('password', 'password') # Default fallback
            email = f"{username}@shelter.local" # Generate dummy email
            
            # Check if user exists
            existing_user = db.query(User).filter(User.username == username).first()
            if existing_user:
                print(f"User {username} already exists. Updating level...")
                existing_user.level = level
                # Optionally update password if we want to sync changes
                # existing_user.password_hash = pwd_context.hash(password)
                skipped_count += 1
            else:
                print(f"Migrating user: {username} (Level {level})")
                new_user = User(
                    username=username,
                    email=email,
                    password_hash=pwd_context.hash(password),
                    level=level,
                    display_name=username,
                    created_at=user_data.get('created_at', datetime.utcnow()),
                    is_active=True,
                    role="user"
                )
                db.add(new_user)
                migrated_count += 1
                
        except Exception as e:
            print(f"Error migrating {user_dir_name}: {e}")
            
    db.commit()
    print(f"Migration complete. Migrated: {migrated_count}, Skipped/Updated: {skipped_count}")

if __name__ == "__main__":
    migrate_users()
