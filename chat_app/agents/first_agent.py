from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai import Agent, RunContext
from typing import Optional
import logfire

from chat_app.tools.vector_store import(
    qdrant_search,
)
from chat_app.tools.client import (
    fetch_users as api_fetch_users,
    fetch_todos as api_fetch_todos,
    fetch_posts as api_fetch_posts,
)

# Configuration is now handled in the main entry point to follow the singleton pattern
model = OllamaModel(
    'qwen2.5:3b',
    provider=OllamaProvider(
        base_url='http://localhost:11434/v1',
    ),
)

first_agent = Agent(
    model,
    system_prompt=(
        "Introduce yourself if the user ask it"
        "You are a ChatBot assistant for users. "
        "Your task is to generate summaries for Users, Posts, and Todos based ONLY on tool results.\n\n"
        
        "SEARCH GUIDELINES:\n"
        "1. Use tool results to find live data.\n"
        "2. If tools return no results, state: 'No records found matching your query.'\n"
        "3. NEVER invent data. NEVER type JSON. NEVER explain your process.\n"
        "4. Provide a clear, natural language summary."
    )
)

@first_agent.tool
async def search_knowledge_base(
    ctx: RunContext[None],
    query:str
    
)->str:
    
    try:
        results = await qdrant_search(query)
        
        if not results:
            return f"no {results} Found"
        
        summary = "\n".join([
            f"Source ID: {rest.get('id', 'Unknown')} | Title: {rest.get('title', 'Unknown')}\n"
            f"Content: {rest.get('body', rest.get('text', 'No content available'))}"
            for rest in results
        ])
        
        return f"Found relevant historical information:\n{summary}"
    except Exception as e:
        logfire.error(f"Tool call search_knowledge_base Failed: {str(e)}")
        
        return f"error using the seach_knowledge_base"

@first_agent.tool
async def search_user_records(
    ctx: RunContext[None],
    username: Optional[str] = None,
    name: Optional[str] = None,
    email: Optional[str] = None,
    website: Optional[str] = None,
) -> str:

    try:

        params = {k: v for k, v in {
            "username": username,
            "name": name,
            "email": email,
            "website": website
        }.items() if v is not None}

        if not params:
            return "No search criteria provided for user search."

        users = await api_fetch_users(**params)
        
        if not users:
            return "No users found matching those criteria."

        summary = "\n".join([
            f"ID: {u.id} | Name: {u.name} | Email: {u.email} | Company: {u.company.name}"
            for u in users
        ])
        return f"Found {len(users)} user(s):\n{summary}"
    
    except Exception as e:
        logfire.error(f"Agent tool 'search_user_records' failed: {str(e)}")
        return "An error occurred while searching for user records."

@first_agent.tool
async def search_todo_records(
    ctx: RunContext[None],
    title: Optional[str] = None,
    completed: Optional[bool] = None,
) -> str:

    try:
        params = {k: v for k, v in {
            "title": title,
            "completed": completed
        }.items() if v is not None}

        if not params:
            return "No search criteria provided for todo search."

        todos = await api_fetch_todos(**params)
        
        if not todos:
            return "No todos found matching those criteria."

        summary = "\n".join([
            f"ID: {t.id} | Title: {t.title} | Completed: {t.completed}"
            for t in todos
        ])
        return f"Found {len(todos)} todo(s):\n{summary}"
    
    except Exception as e:
        logfire.error(f"Agent tool 'search_todo_records' failed: {str(e)}")
        return "An error occurred while searching for todo records."

@first_agent.tool
async def search_post_records(
    ctx: RunContext[None],
    title: Optional[str] = None,
    userId: Optional[int] = None,
) -> str:

    try:
        params = {k: v for k, v in {
            "title": title,
            "userId": userId
        }.items() if v is not None}

        posts = await api_fetch_posts(**params)
        
        if not posts:
            return "No posts found matching those criteria."

        summary = "\n".join([
            f"ID: {p.id} | Title: {p.title} | Body: {p.body[:50]}..."
            for p in posts
        ])
        return f"Found {len(posts)} post(s):\n{summary}"
    
    except Exception as e:
        logfire.error(f"Agent tool 'search_post_records' failed: {str(e)}")
        return "An error occurred while searching for post records."
