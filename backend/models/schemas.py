from pydantic import BaseModel

class Song(BaseModel):
    id: int 
    artista: str
    titulo: str
    imagen: str