"""Configurações gerais da aplicação."""

from pathlib import Path

DIRETORIO_RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_BANCO_DADOS = DIRETORIO_RAIZ / "dados" / "loja.sqlite"
CAMINHO_ESQUEMA_SQL = Path(__file__).resolve().parent / "banco_dados" / "esquema.sql"
