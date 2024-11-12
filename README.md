# Download de Música do Spotify

Este projeto permite que você baixe músicas do Spotify utilizando uma API FastAPI e uma interface web simples.

## Requisitos

- Python 3.7+
- FastAPI
- Spotipy
- ytmdl
- Uvicorn

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Crie um ambiente virtual e ative-o:

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure as variáveis de ambiente para o Spotify:

    ```bash
    export SPOTIFY_CLIENT_ID='seu_client_id'
    export SPOTIFY_CLIENT_SECRET='seu_client_secret'
    ```

    No Windows, use `set` em vez de `export`.

## Executando o Servidor

Inicie o servidor FastAPI:

```bash
uvicorn main:app --reload
```

# Download de Música do Spotify

## O servidor estará disponível em
http://127.0.0.1:8000.

## Interface Web
Abra o arquivo `index.html` em seu navegador para acessar a interface web.

## Endpoints

### POST /download/
Baixa uma música do Spotify.

#### Parâmetros
- `id_` (string): O ID da música do Spotify.

#### Exemplo de Requisição
```bash
curl -X POST "http://127.0.0.1:8000/download/" -H "Content-Type: application/json" -d '{"id_": "spotify_track_id"}'
```


