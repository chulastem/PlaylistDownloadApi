from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import subprocess
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações do Spotify (utilizando variáveis de ambiente)
client_id = os.getenv('SPOTIFY_CLIENT_ID', 'c83b7fd3c3704e30b1fb5c69e23a4b82')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET', 'd1479f72d1614e5488675aafa56322ad')

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

DOWNLOAD_DIR = '/downloads/'

class DownloadRequest(BaseModel):
    id_: str

@app.post("/download/")
async def download(request: DownloadRequest, background_tasks: BackgroundTasks):
    id_song = request.id_

    try:
        # Busca informações da música
        track = sp.track(id_song)
        name = track['name']

        # Baixa o arquivo para o diretório de downloads
        file_path = download_by_link(name, id_song, DOWNLOAD_DIR)

        # Verifica se o arquivo foi baixado com sucesso
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="Erro ao baixar a música.")

        # Agende a exclusão do arquivo após o envio
        background_tasks.add_task(remove_file, file_path)

        # Retorna o arquivo para o cliente com o nome configurado para download
        return FileResponse(
            path=file_path,
            filename=f"{name}.mp3",         # Nome do arquivo para o download no navegador
            media_type="audio/mpeg",        # Tipo de mídia adequado para mp3
            headers={"Content-Disposition": f"attachment; filename={name}.mp3"}  # Força o download no navegador
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

def download_by_link(search_song_title, id_song, download_dir):
    try:
        # Força o uso do diretório especificado, ignorando o cache
        command = f'ytmdl "{search_song_title}" --quiet --output-dir "{os.path.abspath(download_dir)}" --spotify-id "{id_song}"'
        subprocess.call(command, shell=True)

        # Verifica o nome do arquivo baixado no diretório de download
        for file_name in os.listdir(download_dir):
            if search_song_title.lower() in file_name.lower() and file_name.endswith('.mp3'):
                return os.path.join(download_dir, file_name)

        # Caso o arquivo não seja encontrado
        raise HTTPException(status_code=500, detail="Música não encontrada no diretório de download.")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao baixar a música.")

def remove_file(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Erro ao remover o arquivo: {e}")
