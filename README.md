**This is my playground practice for building orchestration and pipeling for Agentic RAG using public API'S**

Docker Setup:
Open the Docker Desktop

run this 
docker compose up -d qdrant
then start the container

if success open this link 
http://localhost:6333/dashboard

then lets start ingesting the api's
docker compose run --rm app uv run python -m chat_app.tools.ingest

run/test it by file
- uv run python -m chat_app.tools.client
