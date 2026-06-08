import os
import asyncio
from rich import print as rprint
from typing import List, Optional, Dict, Any
from qdrant_client import AsyncQdrantClient
from fastembed import TextEmbedding
from qdrant_client.models import Distance, VectorParams


from dotenv import load_dotenv
import logfire

load_dotenv()
logfire.configure()

QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
# QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
QDRANT_COLLECTION_NAME = os.getenv('QDRANT_COLLECTION_NAME')

#Singletons for connection pooling and memory efficient
_qdrant_client: Optional[AsyncQdrantClient] = None
_embedding_model: Optional[TextEmbedding] = None


def get_qdrant_client() -> AsyncQdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = AsyncQdrantClient(
            url=QDRANT_URL,
            # api_key=QDRANT_API_KEY,
        )
    return _qdrant_client

#initializes qdrant collection if it does not exist
def get_embedding_model() -> TextEmbedding:
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    return _embedding_model



async def generate_embedding(text: str) -> List[float]:
    model = get_embedding_model()
    embeddings = list(model.embed([text]))
    return embeddings[0].tolist()



async def init_collection()->None:
    client = get_qdrant_client()
    try:
        exists = await client.collection_exists(collection_name=QDRANT_COLLECTION_NAME) 
        
        if not exists:
            await client.create_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
            
            logfire.info(f"Created new Qdrant collection: {QDRANT_COLLECTION_NAME}")
    except Exception as e:
        logfire.error(f"Failed to initialize qdrant collection: {str(e)}")
        
async def qdrant_search(query:str, limit: int =5) -> List[Dict[str, Any]]:
    
    try:
        client = get_qdrant_client()
        query_vector = await generate_embedding(query)
        
        search_result = await client.search(
            collection_name = QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit,
        )
        
        results = [hit.payload for hit in search_result if hit.payload is not None]
        logfire.info(f"Qdrant search successful: {query} returns {len(results)} results")
        return results
        
    except Exception as e:
        logfire.error(f'qdrant search failed: {str(e)}')
        return []
    

# if __name__ == "__main__":
#     get_embed = asyncio.run(get_embedding_model())
#     rprint(get_embed)