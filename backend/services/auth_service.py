"""
    Módulo empleado para la autenticación en el sistema.
"""

from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv
import os
import requests
import base64

# Configuración de variables de entorno
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET_ID")
REDIRECT_URI_BACKEND = os.getenv("REDIRECT_URI_BACKEND")
REDIRECT_URI_FRONTEND = os.getenv("REDIRECT_URI_FRONTEND")
DEVICE_ID = os.getenv("DEVICE_ID")


def redirect_url_auth()->RedirectResponse:
    """
        Función encargada de redireccionar al inicio de sesión de Spotify
        Una vez que se inicia sesión, se obtiene un código de autorización 
        que debe ser utilizado para obtener un token de acceso a la API.
    """

    url = "https://accounts.spotify.com/authorize?"
    url += "client_id=" + CLIENT_ID
    url += "&response_type=code"
    url += "&redirect_uri=" + REDIRECT_URI_FRONTEND
    url += "&show_dialog=true"
    url += "&scope=user-modify-playback-state,user-read-private"

    return RedirectResponse(url)


def get_access_token(code: str)->dict:
    """
        Función que permite obtener un token de acceso a la API.
        Parámetros de entrada:
            - code (str): Código de autorización obtenido en el inicio de sesión
            que puede ser intercambiado por un token de acceso.

        Devuelve:
            - Diccionario que representa la respuesta obtenida 
    """

    client_credentials = f'{CLIENT_ID}:{CLIENT_SECRET}'
    client_credentials_b64 = base64.b64encode(client_credentials.encode())

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f'Basic {client_credentials_b64.decode()}'
    }

    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI_FRONTEND,
    }

    response = requests.post("https://accounts.spotify.com/api/token", data=body, headers=headers)

    return response.json() 


def check_token(access_token: str):
    """
        Función que permite comprobar si el token de acceso es válido.
        Parámetros de entrada:
            - access_token (str): Token de acceso a la API de Spotify
    """

    headers = {'Content-Type': 'application-json', 'Authorization': f'Bearer {access_token}'}

    response = requests.get("https://api.spotify.com/v1/me", headers=headers)

    if response.status_code == 200:
        return {'valid_token': True}

    else:
        return {'valid_token': False}

