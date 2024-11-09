from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import subprocess
from typing import Optional, List
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações do Spotify
client_id = 'c83b7fd3c3704e30b1fb5c69e23a4b82'
client_secret = 'd1479f72d1614e5488675aafa56322ad'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

DOWNLOAD_DIR = os.path.expanduser("~/Downloads")

class DownloadRequest(BaseModel):
    url: str
    download_dir: Optional[str] = DOWNLOAD_DIR

class Progress:
    current: int = 0
    total: int = 0

progress = Progress()

@app.get("/download_progress")
async def get_progress():
    return {"current": progress.current, "total": progress.total}

@app.post("/download")
async def download(request: DownloadRequest):
    url = request.url
    download_dir = request.download_dir or DOWNLOAD_DIR

    try:
        # Identificar se é playlist, álbum ou faixa
        if "playlist" in url:
            items = sp.playlist_items(url)['items']
        elif "album" in url:
            album = sp.album(url)
            items = album['tracks']['items']
        elif "track" in url:
            items = [{"track": sp.track(url)}]
        else:
            raise HTTPException(status_code=400, detail="URL inválida.")

        progress.total = len(items)
        progress.current = 0

        for item in items:
            track = item['track']
            id_song = track['id']
            song_name = track['name']
            artists = [artist['name'] for artist in track['artists']]
            search_song_title = f"{song_name} - {', '.join(artists)}"

            download_by_link(search_song_title, id_song, download_dir)
            progress.current += 1
        return {"message": "Download started successfully", "directory": download_dir}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def download_by_link(search_song_title, id_song, download_dir):
    try:
        command = f'ytmdl "{search_song_title}" --quiet -o "{download_dir}" --spotify-id "{id_song}"'
        subprocess.call(command, shell=True)
    except Exception as e:
        print(e)
