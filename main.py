"""Script de inicialização do servidor da loja virtual."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:aplicacao", host="127.0.0.1", port=8000, reload=True)
