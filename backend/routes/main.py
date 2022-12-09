from fastapi import FastAPI, Header, Query
from typing import List
from dotenv import load_dotenv
import os
import sys
from services import auth_service, song_service

from fastapi.middleware.cors import CORSMiddleware


# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from models.schemas import Message, Song

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET_ID")
REDIRECT_URI_BACKEND = os.getenv("REDIRECT_URI_BACKEND")
REDIRECT_URI_FRONTEND = os.getenv("REDIRECT_URI_FRONTEND")
DEVICE_ID = os.getenv("DEVICE_ID")

app = FastAPI(title="FastQueue",
description="API para añadir canciones a la cola de Spotify de un dispositivo concreto. Se necesita autenticación vía Spotify para obtener el token de acceso")

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/', include_in_schema=False)
def main():
    return auth_service.redirect_url_auth()


@app.get('/access-token', include_in_schema=False)
def access_token(code: str):
    return auth_service.get_access_token(code)


@app.get('/check-token', include_in_schema=False)
def check_token(access_token: str = Header()):
    return auth_service.check_token(access_token)



@app.get('/search', summary="Búsqueda de canción por título o artista", tags=["Canciones"], response_model=List[Song],
responses={400: {"model": Message, "description":"Id de canción no válido"}, 403: {"model": Message, "description":"Sin permisos"}, 
404: {"model": Message, "description": "Recurso no encontrado"}, 429: {"model": Message, "description":"Sistema saturado"}})
def search(query: str = Query(min_length=1), access_token: str = Header()):
    return song_service.search_song(query, access_token)


@app.post("/add-song-to-queue/{song_id}", summary="Añadir canción a la cola del dispositivo", tags=["Canciones"],
responses={400: {"model": Message, "description":"Id de canción no válido"}, 403: {"model": Message, "description":"Sin permisos"}, 
404: {"model": Message, "description": "Recurso no encontrado"}, 429: {"model": Message, "description":"Sistema saturado"}})
def add_song_to_queue(song_id: str, access_token: str = Header()):
    return song_service.add_song_to_queue(song_id, access_token)




