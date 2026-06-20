import asyncio
import httpx

API_URL = "http://localhost:8000/chat"

async def test_chatbot():
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("query 1: general greeting")
        
        try:
            r1 = await client.post(API_URL, json={"prompt": "Hello introduce yourself briefly"})
            print(f"Status Code: {r1.status_code}")
            print(f"Response: {r1.json().get('response')}\n")
        except Exception as e:
            return (f"Error calling greeting query: {e}\n")
        
        #terst query 2
        print("query 2 api and vector search")
        try:
            r2 = await client.post(API_URL, json={"prompt": "can you check who username Karianne is and search if she has my completed todos?"})
            print(f"status code: {r2.status_code}")
            print(f"response: {r2.json().get('response')}\n")
            
        except Exception as e:
            return (f"Error calling search query: {e}")
        
if __name__ == "__main__":
    asyncio.run(test_chatbot())
    
            