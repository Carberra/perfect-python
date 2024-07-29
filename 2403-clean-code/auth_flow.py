import hashlib
import json
import os
import webbrowser
from pathlib import Path
from urllib.parse import urlencode

import requests

from auth_server import Server

SCOPES = [
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
]
HOST = "localhost"
PORT = 8080


def request_authorisation(secrets: dict[str, str], redirect_uri: str) -> dict[str, str]:
    params = {
        "response_type": "code",
        "client_id": secrets["client_id"],
        "redirect_uri": redirect_uri,
        "scope": " ".join(SCOPES),
        "state": hashlib.sha256(os.urandom(1024)).hexdigest(),
        "access_type": "offline",
    }
    url = f"{secrets['auth_uri']}?{urlencode(params)}"
    if not webbrowser.open(url):
        raise RuntimeError("Failed to open browser")
    return params


def fetch_code(params: dict[str, str]) -> str:
    server = Server(HOST, PORT)
    try:
        server.handle_request()
    finally:
        server.server_close()

    if params["state"] != server.query_params["state"]:
        raise RuntimeError("Invalid state")

    return server.query_params["code"]


def fetch_tokens(
    secrets: dict[str, str], redirect_uri: str, code: str
) -> dict[str, str]:
    params = {
        "grant_type": "authorization_code",
        "client_id": secrets["client_id"],
        "client_secret": secrets["client_secret"],
        "redirect_uri": redirect_uri,
        "code": code,
    }
    with requests.post(
        secrets["token_uri"],
        data=params,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ) as response:
        if response.status_code != 200:
            raise RuntimeError("Failed to authorise")

        return response.json()


def authorise(secrets: dict[str, str]) -> dict[str, str]:
    redirect_uri = f"{secrets['redirect_uris'][0]}:{PORT}"
    params = request_authorisation(secrets, redirect_uri)
    code = fetch_code(params)
    return fetch_tokens(secrets, redirect_uri, code)


if __name__ == "__main__":
    secrets = json.loads(Path("secrets.json").read_text())["installed"]
    tokens = authorise(secrets)
    print(f"Tokens: {tokens}")
