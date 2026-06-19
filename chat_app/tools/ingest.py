import asyncio
import uuid
from rich import print as rprint
from typing import Union, List
from qdrant_client.models import PointStruct
import logfire

from chat_app.tools.client import (
    fetch_users, fetch_todos, fetch_posts, close_client
)
from chat_app.tools.qdrant_client import(
    get_qdrant_client, generate_embedding, 
    init_collection, QDRANT_COLLECTION_NAME
)
from chat_app.schemas.typicode_schema import User, Todo, Post
from chat_app.tools.vector_store import upset_documents
from chat_app.database import close_qdrant_client

#transformation layer: this will convert models to plain text
def transform_to_text(item: Union[User, Todo, Post]) -> str:
    if isinstance(item, User):
        return (f"User Profile: {item.name} (@{item.username})\n"
                f"Email: {item.email}\n"
                f"Address: {item.address.city}"
                f"Company: {item.company.name}"
                f"website: {item.website}"
                )
    elif isinstance(item, Todo):
        status = "Completed" if item.completed else "Pending"
        return(
            f"Task: {item.title}"
            f"Status: {item.completed}"
        )

    
    elif isinstance(item, Post):
        return(
            f"Title: {item.title}\n Body: {item.body}"
        )

    
    return str(item)

#Ingestion Layer: this will orchestrates fetching, embedding, and indexing data
async def run_ingestion():

    await init_collection()
    
    
    q_client = get_qdrant_client()
    
    #fetch data from public api
    data_sources = {
        "users": await fetch_users(),
        "todo": await fetch_todos(),
        "posts": await fetch_posts(),
    }
    
    points = []
    
    for category, items in data_sources.items():
        print (f"{len(items)} {category}")
        
        for item in items:
            text_content = transform_to_text(item)
            
            vector = await generate_embedding(text_content)
            
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{category}_{item.id}"))
            
            points.append(PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "type": category,
                    "original_id": item.id,
                    "text": text_content,
                    **item.model_dump()
                }
            ))
    
    #upsert to qdrant
    # if points:
    #     rprint( f"uploading {len(points)} to qwdrant")
    #     await q_client.upsert(
    #         collection_name=QDRANT_COLLECTION_NAME,
    #         points=points
    #     )
    #     print("Ingestion Completed")
    
    if points: 
        rprint(f"uploading {len(points)} points to qdrant")
        await upset_documents(points)
        rprint("Ingestion Completed")
    else:
        logfire.warning("No data retrieved to ingest")
        
async def main():
    try:
        await run_ingestion()
    finally:
        await close_client()
        await close_qdrant_client()
    
    



if __name__ == '__main__':
    asyncio.run(main())
    