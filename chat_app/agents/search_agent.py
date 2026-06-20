from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai import Agent, RunContext
from chat_app.config import settings
from typing import Optional
import logfire

from chat_app.tools.vector_store import qdrant_search
from chat_app.tools.client import (
    fetch_users as api_fetch_users, 
    fetch_todos as api_fetch_todos, 
    fetch_posts as api_fetch_posts
)

model = OllamaModel(
    settings.default_model,
    provider=OllamaProvider(
        base_url=settings.ollama_base_url,
    ),
)
search_agent = Agent(
    model,
    system_prompt=(
        "You are a Search retrieval specialist. "
        "your task is to fetch relevant records, search the knowledge base, and retrieve raw usert/todo/post details"
        "based only on the tools provided to you."
        "you GUIDELINES: \n"
        "1. Query the vetor knowledge base for semantic queries or context on API entities."
        "2Fetch specific live users, todos, or posts using the live API query tools."
        "3. Provide structure details of the facts you find. DO not synthesic the final user-facing response."
    
    )
)

@search_agent.tool
async def search_knowledge_base(ctx: RunContext[None] , query: str) ->str:
    try:
        results = await qdrant_search(query)
        if not results:
            return "No historical records found matching your query."
        
        summary = "\n".join([
            f"Source ID: {r.get('id', 'Unknown')} | Title: {r.get('title', 'Unknown')}\n"
            f"Content: {r.get('text', r.get('body', 'No content available'))}"
            for r in results
        ])
        return f"Found relevant historical information: \n {summary}"
    except Exception as e:
        logfire.error(f"Search agent failed to search knowledge base: {str(e)}")
        return "error occurred while searching"
    
@search_agent.tool
async def search_user_records(
    ctx: RunContext[None],
    username: Optional[str] = None,
    name: Optional[str] = None,
    email: Optional[str] = None, 
    phone: Optional[str] = None,
    website: Optional[str] = None
)->str:
    try:
         
        params = {key: value for key, value in {
            "username": username,
            "name": name,
            "email": email,
            "phone": phone,
            "website": website
        }.items() if value is not None}
        if not params:
            return "No search criteria provided for user search"
        
        users = await api_fetch_users(**params)
        if not users:
            return "No users found matching those criteria"
        
        summary = "\n".join([
            f"ID: {u.id} | Name: {u.name} | Email: {u.email} | Website: {u.website}"
            for u in users
            
        ])
        return f"Found {len(users)} users:{summary}"
    except Exception as e:
        logfire.error(f"search agent failed to search user records ({str(e)})")
        return "An error occurred while searching user records."

@search_agent.tool 
async def search_todo_records(
    ctx: RunContext[None],
    user_id: Optional[int] = None,
    title: Optional[str] = None,
    completed: Optional[bool] = None
    
)->str:
    
    
    try:
        params = {key: value for key, value in {
            "user_id": user_id, #map to the jsonplaceholder api params
            "title": title,
            "completed": completed
        }.items() if value is not None}
        if not params:
            return "No search criteria provided for todo search"
        
        todo = await api_fetch_todos(**params)
        if not todo:
            return "No todo found matching those criteria"
        
        summary = "\n".join([
            f"title: {t.title} | Completed : {t.completed}"
            for t in todo
        ]) 
        return f"Found {len(todo)} todo(s):\n{summary}"
        
    except Exception as e:
        logfire.error(f"search failed to find todo records: {str(e)}")
        return "An error occurred while searching todo records."
        

@search_agent.tool
async def search_post_records(
    ctx: RunContext[None],
    title: Optional[str] = None,
    body: Optional[str] = None
)->str:
    try:
        params = {key: value for key, value in{
            "title" : title,
            "body": body,
        }.items() if value is not None}
        
        if not params:
            return "No search criteria provided for post search"
        
        post = await api_fetch_posts(**params)
        if not post:
            return "No post matching those criteria"
        
        summary = "\n".join([
            f"title: {p.title}, Body: {p.body}"
            for p in post
        ])
        return f"Found {len(post)} post(s):\n{summary}"
        
    except Exception as e:
        logfire.error(f"Failed to search Post Records: {str(e)}") 
        return "An error occurred while searching post records." 