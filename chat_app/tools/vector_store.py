from typing import Any, Dict, List,Optional
from fastembed import TextEmbedding
from qdrant_client.models import (
    Distance, VectorParams, PointStruct
)
from chat_app.config import settings
from chat_app.database import get_qdrant_client
import logfire

_embedding_model: Optional[TextEmbedding] = None


def get_embedding_model() -> TextEmbedding:
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    return _embedding_model


async def generate_embedding(text:str)->List[float]:
    model = get_embedding_model()
    embeddings = list(model.embed([text]))
    return embeddings[0].tolist()



async def init_collection()->None:
    client = get_qdrant_client()
    collection_name = settings.qdrant_collection_name
    
    try:
        exists = await client.collection_exists(collection_name=collection_name)
        if not exists:
            await client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
            logfire.info(f"Created qdrant collection {collection_name}")
            
        else:
            logfire.error(f"qdrant collection: {collection_name} already exists")
            
    except Exception as e:
        logfire.error(f"Failed to initialize {str(e)}")
        raise e
    
async def qdrant_search(query: str, limit: int =5) -> List[Dict[str, Any]]:
    client = get_qdrant_client()
    collection_name=settings.qdrant_collection_name
    try:
        query_vector = await generate_embedding(query)
        search_result = await client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
        )
        results = [hit.payload for hit in search_result if hit.payload is not None]
        logfire.info(f"Qdrant search successful: {query} return {len(results)} matches")
        return results
    
    except Exception as e:
        logfire.error(f"qdrant search failed {str(e)}")
        
        return []
    
    
async def upsert_documents(points: List[PointStruct]) -> None:
    client = get_qdrant_client()
    collection_name = settings.qdrant_collection_name
    
    try:
        await client.upsert(
            collection_name = collection_name,
            points=points
        )
        
        logfire.info(f"Successfully upserted {len(points)} to {collection_name}")
        
    except Exception as e:
        logfire.error(f"Failed to upsert points into qdrant {str(e)}")