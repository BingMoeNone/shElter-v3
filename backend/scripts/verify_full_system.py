import os
import sys
import logging
from fastapi.testclient import TestClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add backend directory to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(backend_path)
logger.info(f"Added {backend_path} to sys.path")

try:
    from src.main import app
    from src.database.connection import get_db
    logger.info("Successfully imported app and database connection")
except ImportError as e:
    logger.error(f"Failed to import app: {e}")
    sys.exit(1)

client = TestClient(app)

def verify_health():
    logger.info("Verifying Health Check...")
    try:
        response = client.get("/health")
        if response.status_code == 200:
            logger.info("Health check passed: " + str(response.json()))
            return True
        else:
            logger.error(f"Health check failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Health check exception: {e}")
        return False

def verify_database():
    logger.info("Verifying Database Connection...")
    # Health check usually checks DB, but let's try a DB-dependent endpoint
    try:
        # /api/v1/users/ usually requires DB
        response = client.get("/api/v1/users/")
        # It might return 401 if auth is required, or 200 if public list is allowed.
        # Based on typical implementation, it might be protected or empty.
        # Let's check status code. If it's 500, DB is likely down.
        if response.status_code in [200, 401, 403]:
            logger.info(f"Database endpoint responded with {response.status_code} (Expected non-500)")
            return True
        else:
            logger.error(f"Database endpoint failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Database check exception: {e}")
        return False

def verify_articles():
    logger.info("Verifying Articles API...")
    try:
        response = client.get("/api/v1/articles/")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Articles list retrieved. Count: {len(data.get('articles', []))}")
            return True
        else:
            logger.error(f"Articles API failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Articles API exception: {e}")
        return False

def verify_metro():
    logger.info("Verifying Metro API...")
    try:
        response = client.get("/api/v1/metro/lines")
        if response.status_code == 200:
            logger.info(f"Metro lines retrieved: {len(response.json())}")
            return True
        else:
            logger.error(f"Metro API failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Metro API exception: {e}")
        return False

if __name__ == "__main__":
    checks = [
        verify_health(),
        verify_database(),
        verify_articles(),
        verify_metro()
    ]
    
    if all(checks):
        logger.info("\nSUCCESS: All system verifications passed.")
        sys.exit(0)
    else:
        logger.error("\nFAILURE: Some verifications failed.")
        sys.exit(1)
