from fastapi import FastAPI, Header, Query
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

from models.schemas import Song

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET_ID")
REDIRECT_URI_BACKEND = os.getenv("REDIRECT_URI_BACKEND")
REDIRECT_URI_FRONTEND = os.getenv("REDIRECT_URI_FRONTEND")
DEVICE_ID = os.getenv("DEVICE_ID")

app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def main():
    return auth_service.redirect_url_auth()


@app.get('/access-token')
def access_token(code: str):
    return auth_service.get_access_token(code)


@app.post('/search')
def search(query: str = Query(min_length=1), access_token: str = Header()):
    return song_service.search_song(query, access_token)



@app.post("/add-song-to-queue/{song_id}")
def add_song_to_queue(song_id: str, access_token: str = Header()):
    return song_service.add_song_to_queue(song_id, access_token)




