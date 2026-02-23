from src.api.auth import router as auth_router
from src.api.users import router as users_router
from src.api.articles import router as articles_router
from src.api.categories import router as categories_router
from src.api.tags import router as tags_router
from src.api.comments import router as comments_router
from src.api.connections import router as connections_router
from src.api.search import router as search_router
from src.api.media import router as media_router
from src.api.moderation import router as moderation_router

router = auth_router