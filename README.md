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





***Agents purpose***
supervisor_agent.py: first node that runs. it will evaluates the query and determines the search agent (if the prompt asks for live data, searching data) then first_agent if its general greeting like hi, simple chats. and doesnt need data from the qdrant

search_agent.py: interacts with external data sources from the qdrant vector database to fetch requested data.

first_agent.py: the final responder/summarizer. this will synthesizes the final conversational response and npresents it to the user. 


NOTE: i unable to use structured output validation which fails on older Ollama versions, so i will use plain text supervisor. soon i will use newer versions to match our graph and routing