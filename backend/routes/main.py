from fastapi import FastAPI, Request, Header
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os
import requests
import base64
from models.schemas import AccessToken

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")

app = FastAPI()

@app.get('/')
def main():
    url = "https://accounts.spotify.com/authorize?"
    url += "client_id=" + CLIENT_ID
    url += "&response_type=code"
    url += "&redirect_uri=" + REDIRECT_URI
    url += "&show_dialog=true"

    return RedirectResponse(url)


@app.get('/access-token')
def access_token(code: str):


    client_credentials = f'{CLIENT_ID}:{CLIENT_SECRET}'
    client_credentials_b64 = base64.b64encode(client_credentials.encode())

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f'Basic {client_credentials_b64.decode()}'
    }

    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post("https://accounts.spotify.com/api/token", data=body, headers=headers)
    response_json = response.json()
    
    return response_json


@app.post('/search')
#Header with access-token
def search(query: str, access_token: str = Header()):

    headers = {
        "Authorization": f'Bearer {access_token}'
    }

    response = requests.get(f"https://api.spotify.com/v1/search?q={query}&type=track", headers=headers)
    response_json = response.json()

    return response_json

