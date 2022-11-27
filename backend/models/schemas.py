from pydantic import BaseModel

class Song(BaseModel):
    id: str 
    artista: str
    titulo: str
    imagen: str

class AccessToken(BaseModel):
    access_token: str

class Message(BaseModel): 
    message: str