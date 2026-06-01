from pydantic import BaseModel


#typicode api's
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
    
# TODO: Renamed from Todos to Todo for industry standard naming conventions
class Todo(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool
    
    
#POST
class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str
