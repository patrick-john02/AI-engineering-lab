from pydantic_ai import Agent, RunContext
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider


from chat_app.config import settings
from pydantic import BaseModel
from typing import Optional


from chat_app.tools.client import fetch_weather, fetch_location

model = OllamaModel(
    settings.default_model,
    provider=OllamaProvider(
        base_url=settings.ollama_base_url,
    ),
)

weather_forecaster = Agent(
    model,
    system_prompt=(
        "You are a Weather Forecaster that will report about the weather on the given information"
        "your tasks is to fetch about the  weather based on the provided data, use the search_weather_records,"
        "base only on the tools provided to you"
        
        "your GUIDELINE: \n"
        
        "1. query the weather search for calling the api call in realtime"
        "2. Fetch specific live weathers. base on the weather api"
        "3. provide structured details of the facts you find. do not synthesize the final weather facing response"
        )

)

# @weather_forecaster.tool
# async def get_Location(
#     ctx:RunContext,
#     name:str,
#     latitude: float,
#     longitude: float,
#     elevation: float,
#     country_code: str,
#     timezone: str,
#     population: int,
#     country: str,
#     admin1: str,
#     admin2:str,
#     admin3:str,
# )->str:
#     try:
#         params = {key: value for keym value in{
#             "name": name,
#             "latitude": latitude,
#             "longitude": longitude,
#             "elevation": elevation,
#             "country_code":country_code,
#             "timezone":timezone,
#             "population":population,
#             "country":country,
#             "admin1":admin1,
#             "admin2":admin2,
#             "admin3":admin3
#         }.items() if value is not None}
#         if not params:
#             return "no search criteria provided for location search"
        
#         location = await fetch_location(**params)
#         if not location:
#             return "No location found matching those criteria"
        
#         summary = "\n".join([
#             f"latitude"
#         ])
            
        


# @weather_forecaster.tool
# async def search_weather_base(
#     ctx:RunContext[None],
#     latitude: float,
#     longitude: float,
# )->str:
    
#     try:
#         params = {
#             "latitude": latitude,
#             "longitude": longitude,
#             "current_weather": "true"
#         }
        
        
    