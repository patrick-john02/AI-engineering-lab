import httpx
from typing import Any, List, Optional
from pydantic import TypeAdapter
from chat_app.schemas.typicode_schema import User, Todo, Post
from rich import print as rprint
import asyncio
import logfire
import os

logfire.configure()

JSONPLACEHOLDER_URL = os.getenv("JSONPLACEHOLDER_URL", "https://jsonplaceholder.typicode.com")


_http_client: Optional[httpx.AsyncClient] = None

#Returns a AsyncClient instance.
def get_client() -> httpx.AsyncClient:

    global _http_client 
    if _http_client is None:
        _http_client = httpx.AsyncClient(timeout=10.0)
    return _http_client

#Closes the AsyncClient instance.
async def close_client():

    global _http_client
    if _http_client is not None:
        await _http_client.aclose()
        _http_client = None


UserListAdapter = TypeAdapter(List[User])
TodoListAdapter = TypeAdapter(List[Todo])
PostListAdapter = TypeAdapter(List[Post])

async def fetch_users(**params: Any) -> List[User]:

    client = get_client()
    try:
        response = await client.get(f"{JSONPLACEHOLDER_URL}/users", params=params)
        response.raise_for_status()
        validated_data = UserListAdapter.validate_python(response.json())
        logfire.info(f"Successfully retrieved {len(validated_data)} users")
        return validated_data
    except Exception as e:
        logfire.error(f"Failed to fetch users: {str(e)}")
        return []

async def fetch_todos(**params: Any) -> List[Todo]:


    client = get_client()
    try:
        response = await client.get(f"{JSONPLACEHOLDER_URL}/todos", params=params)
        response.raise_for_status()
        validated_data = TodoListAdapter.validate_python(response.json())
        logfire.info(f"Successfully retrieved {len(validated_data)} todos")
        return validated_data
    except Exception as e:
        logfire.error(f"Failed to fetch todos: {str(e)}")
        return []

async def fetch_posts(**params: Any) -> List[Post]:

    client = get_client()
    try:
        response = await client.get(f"{JSONPLACEHOLDER_URL}/posts", params=params)
        response.raise_for_status()
        validated_data = PostListAdapter.validate_python(response.json())
        logfire.info(f"Successfully retrieved {len(validated_data)} posts")
        return validated_data
    except Exception as e:
        logfire.error(f"Failed to fetch posts: {str(e)}")
        return []



# if __name__ == '__main__':
    # users = asyncio.run(fetch_users())
    # todo = asyncio.run(fetch_todos())
    # post = asyncio.run(fetch_posts())
    
    # rprint(todo)