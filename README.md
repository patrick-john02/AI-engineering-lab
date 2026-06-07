Docker Setup:
Open the Docker Desktop

run this 
docker compose up -d qdrant

if success open this link
http://localhost:6333/dashboard

then lets start to ingest the api's
docker compose run --rm app python -m chat_app.ingest

run/test it by file
- uv run python -m chat_app.tools.client
