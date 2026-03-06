# ruff: noqa: E501
"""Script d'initialisation de l'architecture Microservices - Toolbox IA ʕ•ᴥ•ʔ.

Ce script génère automatiquement l'arborescence complète et les fichiers de
configuration pour un projet Python moderne, scalable et conteneurisé.

Architecture générée (3 tiers) :
    - Backend (app_api) : API REST avec FastAPI et SQLAlchemy.
    - Frontend (app_front) : Interface utilisateur avec Streamlit.
    - Database : Service PostgreSQL avec persistance des données.

Outils et standards intégrés :
    - Gestionnaire de dépendances : uv
    - Qualité du code : Ruff (Linting & Formatage)
    - Tests : Pytest (avec rapport de couverture)
    - Orchestration : Docker & Docker Compose (Réseaux isolés)
    - CI/CD : GitHub Actions (Quality Gate, Déploiement Docker, GitHub Pages)
    - Documentation technique : Sphinx (thème Furo)

Utilisation :
    1. Placer ce script dans un dossier vide.
    2. Exécuter : `python init-project.py`
    3. Installer l'environnement : `uv sync`
    4. Lancer l'infrastructure : `docker compose up --build`
"""

import os
import shutil
import sys  # noqa: F401 - Conservé pour une future gestion des codes d'erreur (sys.exit)
from pathlib import Path

# Codes de couleur ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
NC = "\033[0m"


def check_prerequisites():
    """Vérifie que les outils nécessaires sont installés sur le système."""
    missing_tools = []

    if shutil.which("uv") is None:
        missing_tools.append("uv (https://github.com/astral-sh/uv)")
    if shutil.which("docker") is None:
        missing_tools.append("docker (https://www.docker.com/)")

    if missing_tools:
        print(f"{RED}[ERREUR FATALE]{NC} Outils manquants pour l'architecture :")
        for tool in missing_tools:
            print(f"  - {tool}")
        print(f"{YELLOW}Veuillez les installer avant de lancer ce script.{NC}")
        sys.exit(1)  # C'est ici que l'on coupe le programme proprement !


def create_file(path, content="", is_executable=False):
    """Crée un fichier avec gestion d'erreur et de permissions."""
    try:
        parent = Path(path).parent
        if not parent.exists():
            parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

        if is_executable:
            os.chmod(path, 0o755)

        print(f"{GREEN}[OK]{NC} Fichier créé : {CYAN}{path}{NC}")
    except Exception as e:
        print(f"{RED}[ERREUR]{NC} Échec de création du fichier {path} : {e}")


def setup_microservices():
    """Initialise l'arborescence complète Microservices IA."""
    print(f"{CYAN}ʕ•ᴥ•ʔ Initialisation de l'architecture Microservices Complète...{NC}")

    # ==========================================
    # 1. CRÉATION DES DOSSIERS ET __init__.py
    # ==========================================
    directories = [
        "app_api/maths",
        "app_api/models",
        "app_api/modules",
        "app_front",
        "tests",
        "docs/source/_static",
        ".github/workflows",
    ]

    for folder in directories:
        Path(folder).mkdir(parents=True, exist_ok=True)
        init_path = Path(folder) / "__init__.py"

        # Gestion spécifique pour le modèle (Correction Ruff F401)
        if folder == "app_api/models":
            doc = '"""Package SQLAlchemy avec ré-export."""\n\nfrom .database import Base as Base\n'
        else:
            doc = f'"""Package {folder.replace("/", ".")}."""\n'

        create_file(str(init_path), doc)

    create_file("app_api/__init__.py", '"""Package principal FastAPI."""\n')

    # ==========================================
    # 2. FICHIERS RACINE (Orchestration & Config)
    # ==========================================

    # pyproject.toml
    pyproject = """[project]
name = "toolbox_ia_microservice"
version = "1.0.0"
description = "Architecture Microservices IA conteneurisée avec FastAPI, Streamlit et PostgreSQL"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastapi",
    "uvicorn[standard]",
    "sqlalchemy",
    "psycopg2-binary",
    "streamlit",
    "requests",
    "pydantic-settings",
    "loguru"
]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.15.4",
    "genbadge[all]>=1.1.0",
    "sphinx",
    "furo",
    "myst-parser"
]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
# E, F : Erreurs PEP8 et logiques
# I : Tri des imports (isort)
# D : Vérification des docstrings
select = ["E", "F", "I", "D"]
ignore = [
    "D100", # Missing docstring in public module (souvent redondant)
    "D203", # one-blank-line-before-class
    "D213", # multi-line-summary-second-line
]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
# Génère automatiquement le rapport de couverture pour l'API
addopts = "-v --cov=app_api --cov-report=term-missing --cov-report=xml"

[tool.coverage.run]
source = ["app_api"]
omit = ["tests/*", "**/__init__.py"]
"""
    create_file("pyproject.toml", pyproject)

    # docker-compose.yml
    compose = """services:
  db:
    image: postgres:15-alpine
    container_name: db-1
    env_file: .env
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - back-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d toolbox"]
      interval: 5s
      timeout: 5s
      retries: 5

  api:
    build: ./app_api
    container_name: api-1
    depends_on:
      db:
        condition: service_healthy
    env_file: .env
    networks:
      - back-net
      - front-net

  front:
    build: ./app_front
    container_name: front-1
    ports:
      - "8501:8501"
    depends_on:
      - api
    env_file: .env
    networks:
      - front-net

networks:
  back-net:
  front-net:

volumes:
  postgres_data:
"""
    create_file("docker-compose.yml", compose)

    # Variables d'environnement
    create_file(
        ".env",
        "POSTGRES_USER=user\nPOSTGRES_PASSWORD=password\nPOSTGRES_DB=toolbox\nDATABASE_URL=postgresql://user:password@db:5432/toolbox\nAPI_URL=http://api:8000",
    )
    create_file(
        ".gitignore",
        "venv/\n.venv/\n__pycache__/\n.env\n.pytest_cache/\n.ruff_cache/\n",
    )
    create_file(
        ".dockerignore",
        "venv/\n.venv/\n__pycache__/\n.pytest_cache/\ndocs/\ntests/\n.git/",
    )

    # Script de nettoyage
    clean = """#!/bin/bash
echo "ʕ•ᴥ•ʔ Nettoyage de l'architecture..."
docker compose down -v
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name ".pytest_cache" -exec rm -rf {} +
find . -type d -name ".ruff_cache" -exec rm -rf {} +
echo "✅ Environnement réinitialisé !"
"""
    create_file("clean_project.sh", clean, is_executable=True)

    # ==========================================
    # 3. SERVICE BACKEND (API)
    # ==========================================

    api_docker = """FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
# Installation système pour psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev
COPY app_api/ ./app_api/
ENV PYTHONPATH="."
CMD ["uv", "run", "uvicorn", "app_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    create_file("app_api/Dockerfile", api_docker)
    create_file(
        "app_api/maths/mon_module.py",
        '"""Module de calcul mathématique."""\n\ndef add(a: float, b: float) -> float:\n    """Additionne deux nombres."""\n    return a + b\n',
    )
    create_file(
        "app_api/models/database.py",
        '"""Définition des tables SQLAlchemy."""\nfrom sqlalchemy.orm import declarative_base\n\nBase = declarative_base()\n',
    )

    api_main = """\"\"\"Point d'entrée de l'API FastAPI avec monitoring Loguru.\"\"\"
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from loguru import logger
import sys
import time

# Imports internes
from app_api.maths.mon_module import add
from app_api.models.database import Base, Calcul
from app_api.modules.connect import engine, get_db

# Configuration de Loguru (Corrigée pour E501)
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan> - "
    "<level>{message}</level>"
)

logger.remove()
logger.add(sys.stdout, format=LOG_FORMAT, level="INFO")

# Création des tables
try:
    Base.metadata.create_all(bind=engine)
    logger.success("Initialisation de la base de données réussie.")
except Exception as e:
    logger.critical(f"Impossible d'initialiser la base de données : {e}")

app = FastAPI(title="Toolbox IA API")

@app.on_event("startup")
def startup():
    \"\"\"Action au démarrage de l'API (Corrigée pour D103).\"\"\"
    logger.info("ʕ•ᴥ•ʔ Microservice API prêt à l'emploi.")

@app.get("/compute/add")
def compute_add(a: float, b: float, db: Session = Depends(get_db)):
    \"\"\"Calcule l'addition et persiste le résultat avec traçabilité.\"\"\"
    start_time = time.time()
    logger.info(f"Requête reçue : addition de {a} et {b}")

    try:
        res = add(a, b)
        nouveau_calcul = Calcul(a=a, b=b, resultat=res)
        db.add(nouveau_calcul)
        db.commit()
        
        duration = time.time() - start_time
        logger.success(f"Calcul sauvegardé : {res} (Temps : {duration:.4f}s)")
        
        return {"result": res, "saved": True, "duration": duration}

    except Exception as e:
        db.rollback()
        logger.exception("Erreur lors du calcul ou de l'enregistrement en base")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/data")
def get_history(db: Session = Depends(get_db)):
    \"\"\"Récupère l'historique avec monitoring de charge.\"\"\"
    logger.debug("Consultation de l'historique demandée")
    try:
        historique = db.query(Calcul).all()
        logger.info(f"Historique récupéré : {len(historique)} entrées trouvées")
        return historique
    except Exception as e:
        logger.error(f"Échec de la récupération des données : {e}")
        raise HTTPException(status_code=500, detail="Base de données inaccessible")
"""
    create_file("app_api/main.py", api_main)

    # ==========================================
    # 4. SERVICE FRONTEND (Streamlit)
    # ==========================================

    front_docker = """FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev
COPY app_front/ ./app_front/
CMD ["uv", "run", "streamlit", "run", "app_front/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
    create_file("app_front/Dockerfile", front_docker)

    front_main = """\"\"\"Interface Utilisateur Streamlit - Toolbox IA ʕ•ᴥ•ʔ.\"\"\"
import os
import sys
import requests
import streamlit as st
from loguru import logger

# Configuration de Loguru pour le Frontend
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan> - <level>{message}</level>"
)
logger.remove()
logger.add(sys.stdout, format=LOG_FORMAT, level="INFO")

# Configuration de l'URL API
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def run_app():
    \"\"\"Exécute l'interface Streamlit avec monitoring Loguru.\"\"\"
    st.set_page_config(page_title="Toolbox IA", page_icon="ʕ•ᴥ•ʔ")
    st.title("Toolbox IA - Interface")

    # --- Calculateur ---
    st.header("Calculateur Magique")
    a = st.number_input("Nombre A", value=0.0)
    b = st.number_input("Nombre B", value=0.0)

    if st.button("Calculer"):
        logger.info(f"Utilisateur demande calcul : {a} + {b}")
        try:
            res = requests.get(f"{API_URL}/compute/add", params={"a": a, "b": b}, timeout=5)
            if res.status_code == 200:
                resultat = res.json().get('result')
                st.success(f"Résultat : {resultat}")
                logger.success(f"Calcul réussi : {resultat}")
            else:
                st.error("L'API a répondu avec une erreur.")
                logger.error(f"Erreur API : Status Code {res.status_code}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")
            logger.exception("Échec de connexion au service Backend")

    st.markdown("---")

    # --- Historique ---
    st.header("Historique")
    if st.button("Afficher la base de données"):
        logger.info("Consultation de l'historique DB demandée")
        try:
            res = requests.get(f"{API_URL}/data", timeout=5)
            data = res.json()
            st.table(data)
            logger.info(f"Historique affiché : {len(data)} entrées")
        except Exception as e:
            st.warning("Impossible de récupérer l'historique.")
            logger.error(f"Échec récupération historique : {e}")

if __name__ == "__main__":
    run_app()
"""
    create_file("app_front/main.py", front_main)

    # ==========================================
    # 5. TESTS ET RÉSOLUTION DES IMPORTS
    # ==========================================

    conftest = """\"\"\"Configuration Pytest pour résoudre les imports absolus.\"\"\"
import sys
import os

# Ajoute la racine du projet au PYTHONPATH pour trouver app_api/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
    create_file("tests/conftest.py", conftest)

    test_maths = """\"\"\"Tests unitaires pour la logique mathématique.\"\"\"
from app_api.maths.mon_module import add

def test_add():
    \"\"\"Test la fonction d'addition.\"\"\"
    assert add(2, 3) == 5
"""
    create_file("tests/test_maths.py", test_maths)

    # ==========================================
    # 6. GITHUB ACTIONS (CI & CD)
    # ==========================================

    ci = """name: CI Quality Check
on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
      - name: Set up Python
        run: uv python install 3.12
      - name: Install dependencies
        run: uv sync
      - name: Lint with ruff
        run: uv run ruff check .
      - name: Tests & Coverage Badge
        run: |
          PYTHONPATH=. uv run pytest --cov=app_api --cov-report=xml
          mkdir -p docs/source/_static
          uv run genbadge coverage -i coverage.xml -o docs/source/_static/coverage.svg
      - name: Save Badge
        uses: actions/upload-artifact@v4
        with:
          name: coverage-badge
          path: docs/source/_static/coverage.svg

  deploy-docs:
    needs: quality-gate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync
      - uses: actions/download-artifact@v4
        with:
          name: coverage-badge
          path: docs/source/_static/
      - name: Build Docs
        run: uv run sphinx-build docs/source public
      - uses: actions/upload-pages-artifact@v3
        with:
          path: public/
      - id: deployment
        uses: actions/deploy-pages@v4
"""
    create_file(".github/workflows/ci.yml", ci)

    # [Note pour Anna] : On utilise GHCR.io pour éviter de gérer des secrets DockerHub.
    # Le pipeline CD ne se déclenche que si le pipeline CI (nommé ici "CI Pipeline - Toolbox V2") réussit.
    cd_content = """
name: CD Pipeline - Livraison GHCR

on:
  workflow_run:
    workflows: ["CI Pipeline - Toolbox V2"]
    types:
      - completed
    branches:
      - main

jobs:
  build-and-push:
    # On vérifie de manière stricte que le pipeline précédent est "success"
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write

    steps:
      - name: Récupération du code
        uses: actions/checkout@v4

      - name: Connexion au GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build et Push - API
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./app_api/Dockerfile
          push: true
          tags: |
            ghcr.io/${{ github.repository_owner }}/toolbox-api:latest
            ghcr.io/${{ github.repository_owner }}/toolbox-api:${{ github.sha }}

      - name: Build et Push - Front
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./app_front/Dockerfile
          push: true
          tags: |
            ghcr.io/${{ github.repository_owner }}/toolbox-front:latest
            ghcr.io/${{ github.repository_owner }}/toolbox-front:${{ github.sha }}
"""
    create_file(".github/workflows/cd.yml", cd_content)

    # ==========================================
    # 7. SPHINX (Documentation)
    # ==========================================
    conf_py = """import os\nimport sys\nsys.path.insert(0, os.path.abspath('../../'))\n
project = 'Toolbox IA'\nauthor = 'Anna'\nrelease = '1.0'\n
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'myst_parser']\n
html_theme = 'furo'\nhtml_static_path = ['_static']\n"""
    create_file("docs/source/conf.py", conf_py)

    print(f"\n{GREEN}ʕ•ᴥ•ʔ Architecture terminée avec succès !{NC}")
    print(f"{YELLOW}Prochaines étapes :{NC}")
    print(f"1. {CYAN}uv sync{NC} (Pour installer les dépendances et créer le lockfile)")
    print(f"2. {CYAN}docker compose up --build{NC} (Pour lancer l'infrastructure)")


if __name__ == "__main__":
    try:
        check_prerequisites()  # On vérifie le système d'abord
        setup_microservices()  # On lance la création
    except KeyboardInterrupt:
        # Gère le cas où l'utilisateur fait Ctrl+C
        print(f"\n{YELLOW}[!] Interruption détectée. Arrêt du script.{NC}")
        sys.exit(0)
    except Exception as e:
        # Gère n'importe quel autre bug inattendu
        print(f"\n{RED}[CRASH]{NC} Une erreur inattendue est survenue : {e}")
        sys.exit(1)
