# """
# Ce Document sert à créer la structure du projet.
#  Avec les files et directories ci-dessous.
#    .
#    ├── app/                   # Code source de l'application
#    ├── tests/                 # Tests unitaires et d'intégration (Pytest)
#    ├── docs/                  # Documentation technique (Sphinx/Furo)
#    ├── pyproject.toml         # Configuration centralisée des outils
#    ├── uv.lock                # Verrouillage des dépendances (généré par uv)
#    ├── Dockerfile             # Conteneurisation de l'application
#    └── README.md              # Vitrine du projet (Badges, Infos, Guide)
#  Puis le `uv sync` pour initialiser.
#  Et le Read The Docs pour la documentation.
# """

import sys
from pathlib import Path

# Codes de couleur ANSI pour le terminal
RED = "\033[0;31m"  # Rouge : Erreurs critiques
GREEN = "\033[0;32m"  # Vert : Succès / Validations
YELLOW = "\033[1;33m"  # Jaune : Avertissements / Infos importan
BLUE = "\033[0;34m"  # Bleu : Titres / Sections
CYAN = "\033[0;36m"  # Cyan : Détails techniques (chemins, fichiers
NC = "\033[0m"  # Reset


def create_file(path, content=""):
    """Crée un fichier avec gestion d'erreur intégrée."""
    try:
        # Vérification si le dossier parent existe
        parent = Path(path).parent
        if not parent.exists():
            parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"{GREEN}[OK]{NC} Fichier créé : {CYAN}{path}{NC}")
    except PermissionError:
        print(f"{RED}[ERREUR]{NC} Droits insuffisants pour créer le fichier : {path}")
    except Exception as e:
        print(f"{RED}[ERREUR]{NC} Échec de création du fichier {path} : {e}")


def setup_toolbox():
    """Initialise l'arborescence et les fichiers de configuration du projet.

    Cette fonction crée les dossiers standards, génère le pyproject.toml,
    le Dockerfile et les workflows GitHub Actions.
    """
    # 1. Définition de l'arborescence cible
    structure = [
        "app",
        "app/modules",
        "tests",
        "docs/source",
        ".github/workflows",
    ]

    # Contenu des docstrings pour les fichiers __init__.py
    docstrings = {
        "app": '"""Package principal de l\'application SQLalchemy Exo."""\n',
        "app/modules": '"""Package contenant les modules de logique métier."""\n',
        "tests": '"""Package contenant la suite de tests automatisés."""\n',
    }

    print(f"{CYAN}ʕ•ᴥ•ʔ Initialisation de la structure professionnelle...{NC}")

    for folder in structure:
        try:
            Path(folder).mkdir(parents=True, exist_ok=True)
            print(f"{GREEN}[OK]{NC} Dossier prêt : {CYAN}{folder}{NC}")
            # Création des __init__.py pour les dossiers de code
            # On vérifie si c'est 'app', 'tests' ou un sous-module
            if folder in ["app", "app/modules", "tests"]:
                init_path = Path(folder) / "__init__.py"
                if not init_path.exists():
                    # On écrit la docstring correspondante dans le fichier
                    content = docstrings.get(folder, "")
                    with open(init_path, "w", encoding="utf-8") as f:
                        f.write(content)
        except Exception as e:
            print(f"{RED}[ERREUR]{NC} Impossible de créer le dossier {folder} : {e}")
            # On continue pour tenter de créer le reste, ou sys.exit(1) si critique

    # 2. Création du pyproject.toml centralisé
    pyproject_content = """
[project]
name = "sqlalchemy-exo"
version = "0.1.0"
description = "Toolbox de référence pour le cursus IA"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "pandas",
    "pytest",
    "pytest-cov",
    "ruff",
    "sphinx",
    "furo",
    "myst-parser",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["app*"]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "D"]
ignore = [
    "D100", # Autorise l'absence de docstring en haut du script principal
    "D203", # Utilise D211 (no-blank-line-before-class) à la place
    "D213", # Utilise D212 (multi-line-summary-first-line) à la place
]

[tool.coverage.run]
omit = ["app/main.py"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
pythonpath = ["."]
addopts = "-v --cov=app --cov-report=term-missing"
"""
    create_file("pyproject.toml", pyproject_content)

    # 3. Création du Dockerfile (Léger et optimisé)
    docker_content = """
FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY . .
RUN uv sync --frozen

# Ajout du chemin pour que le package 'app' soit reconnu
ENV PYTHONPATH="."

CMD ["uv", "run", "app/main.py"]
"""
    create_file("Dockerfile", docker_content)

    # 4. Création du Workflow CI GitHub Actions
    ci_content = """
name: CI Quality Check
on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v3
      - name: Lint with ruff
        run: uv run ruff check .
      - name: Run tests
        run: uv run pytest
"""
    create_file(".github/workflows/ci.yml", ci_content)

    # 5. Création des fichiers de gouvernance (Standard GitHub)
    create_file(".github/CONTRIBUTING.md", "# Guide de contribution")
    create_file(".github/CODE_OF_CONDUCT.md", "# Code de conduite")
    create_file("LICENSE", "MIT License")
    create_file(
        "README.md",
        "# Toolbox\n\nBienvenue dans le template professionnel.",
    )

    print(f"\n{CYAN}ʕ•ᴥ•ʔ Arborescence et configurations créées avec succès.{NC}")
    print(
        f"{CYAN}ʕ•ᴥ•ʔ Prochaine étape : 'uv sync' pour installer l'environnement.{NC}"
    )


if __name__ == "__main__":
    try:
        setup_toolbox()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Interruption détectée. Arrêt du script.{NC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}[ERREUR FATALE]{NC} Une erreur inattendue est survenue : {e}")
        sys.exit(1)
