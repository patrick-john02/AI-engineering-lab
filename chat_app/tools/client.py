import httpx, asyncio, json
from typing import Any, List, Dict
from dotenv import load_dotenv
from pydantic import BaseModel
import logfire
import os

load_dotenv()
logfire.configure()

JSONPLACEHOLDER_URL = os.getenv("JSONPLACEHOLDER_URL", "https://jsonplaceholder.typicode.com")

class Geo(BaseModel):
    lat: float
    lng: float

class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo
    
class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str

class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: Address
    phone: str
    website: str
    company: Company
    


#searches records using dynamic query parameters
async def search_user_records(**query_params:Any) -> List[User]:
    if not query_params:
        logfire.warn("No search parameters provided.")
        
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{JSONPLACEHOLDER_URL}/users",
                params=query_params,
                timeout=5.0
            )
            response.raise_for_status()
            
            raw_users = response.json()
            
            validated_users = [User(**user_dict) for user_dict in raw_users]
            logfire.info(f"Retrieved {len(validated_users)}")
            
            return validated_users
        
        
        except httpx.HTTPStatusError as exc:
            logfire.erro(f"HTTP {exc.response.status_code} error requesting {exc.request.url}")
            raise
            
        except httpx.RequestError as exc:
            logfire.error(f"Network error occurred requesting {exc.request.url}")
            raise
        
if __name__ == "__main__":
    users = asyncio.run(search_user_records(username="Bret"))
    if users:
        target_user = users[0]
        
        print(f"Name: {target_user.name}")
        print(f"Company Name: {target_user.company.name}")
        
        print(f"Latitude (as Float): {target_user.address.geo.lat}")
        print(f"Latitude Type: {type(target_user.address.geo.lat)}")
    else:
        print("User not found.")