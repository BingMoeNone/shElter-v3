import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import User
from src.auth.jwt import get_password_hash


def create_admin():
    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "114514@bingmoe.com").first()
        if existing:
            print(f"绠＄悊鍛樺凡瀛樺湪: {existing.username} ({existing.email})")
            existing.role = "admin"
            db.commit()
            print("宸叉洿鏂颁负绠＄悊鍛樻潈闄?)
            return
        
        admin = User(
            username="BingMoeNone",
            email="114514@bingmoe.com",
            password_hash=get_password_hash("bingmoe@"),
            display_name="BingMoeNone",
            role="admin",
            is_active=True,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"绠＄悊鍛樺垱寤烘垚鍔?")
        print(f"  鐢ㄦ埛鍚? {admin.username}")
        print(f"  閭: {admin.email}")
        print(f"  瑙掕壊: {admin.role}")
    except Exception as e:
        print(f"鍒涘缓绠＄悊鍛樺け璐? {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
