from typing import Optional
from qdrant_client import AsyncQdrantClient
from chat_app.config import settings
import logfire

_qdrant_client: Optional[AsyncQdrantClient] = None

def get_qdrant_client() -> AsyncQdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = AsyncQdrantClient(
            url=settings.qdrant_url,
            # api_key=settings.qdrant_api_key,
        )
        logfire.info("Qdrant async success!")
    return _qdrant_client

async def close_qdrant_client() -> None:
    global _qdrant_client
    if _qdrant_client is not None:
        await _qdrant_client.close()
        logfire.info("Qdrant connection is closed")
        _qdrant_client=None
        
        