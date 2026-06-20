Run and Test Instructions

Follow these steps to run and test the complete pipeline:

1.Start Qdrant:

docker compose up -d qdrant


2.Ingest API Entities into Qdrant
Run the ingestion script to fetch users, todos, and posts from the API, embed them, and index them in Qdrant:

uv run python -m chat_app.tools.ingest

3. run ollama

if already installed 
ollama run qwen2.5:3b or 7b (change the model on the code if ever you choose 7b)


3. Run the FastAPI App Server
Start the API backend at port 8000:

uv run uvicorn main:app --reload --port 8000


4. testing

uv run python -m chat_app.client_test
