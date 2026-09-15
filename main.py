"""Script de inicialização do servidor da loja virtual."""

import os

import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    porta = int(os.getenv("PORT", "8000"))
    recarregar_automaticamente = os.getenv("RELOAD", "true").lower() == "true"

    uvicorn.run("app.main:aplicacao", host=host, port=porta, reload=recarregar_automaticamente)
