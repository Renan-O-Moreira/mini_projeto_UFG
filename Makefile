# Makefile da Loja UFG — instalação, execução e testes com um único comando.
# Compatível com Linux e macOS (requer "make" e "python3" disponíveis no PATH).

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: install run test clean

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt -r requirements-dev.txt

run:
	$(PYTHON) main.py

test:
	$(VENV)/bin/pytest testes/ -v

clean:
	rm -rf $(VENV) dados/loja.sqlite .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
