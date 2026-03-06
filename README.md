# Toolbox IA - Architecture Microservices de Anna

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg?style=for-the-badge)

![CI Status](https://github.com/AnnaVitry/Toolbox_IA_Anna/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![Coverage](https://annavitry.github.io/Toolbox_IA_Anna/_static/coverage.svg)](https://annavitry.github.io/Toolbox_IA_Anna/)

Ce projet est une plateforme de services IA **multi-tiers** conteneurisée. Elle orchestre une interface utilisateur, une API de calcul et une base de données persistante PostgreSQL.

---

## ʕ•ᴥ•ʔっ · · · ✴ Architecture du Projet

L'écosystème est découpé en trois services autonomes communiquant via des réseaux isolés :

* **Frontend (Streamlit)** : Interface utilisateur pour la saisie et la visualisation des données.
* **Backend (FastAPI)** : Logique métier, calculs mathématiques et orchestration des données.
* **Database (PostgreSQL)** : Stockage persistant des historiques via volumes Docker.

---

## ʕ•ᴥ•ʔっ · · · ✴ Marche à suivre : Installation

Assurez-vous d'avoir [Docker](https://www.docker.com/) et [Docker Compose](https://docs.docker.com/compose/) installés.

### 1. Clonage du projet

```bash
git clone https://github.com/AnnaVitry/Toolbox_IA_Microservice.git
cd Toolbox_IA_Microservice

```

### 2. Configuration (Optionnel)

Créez un fichier `.env` à la racine si vous souhaitez personnaliser les identifiants de la base de données.

### 3. Déploiement

Lancez l'orchestration complète :

```bash
docker compose up --build

```

* **Frontend** : [http://localhost:8501](https://www.google.com/search?q=http://localhost:8501)
* **API (Swagger)** : [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)

---

## ʕ•ᴥ•ʔっ · · · ✴ Commandes de Maintenance

Utilisez ces outils pour garantir l'excellence technique du projet.

### Hygiène & Réinitialisation

Pour supprimer proprement les conteneurs, les volumes (RAZ de la DB) et les caches Python :

```bash
chmod +x clean_project.sh
./clean_project.sh

```

### Qualité du Code (Linting)

Vérifiez la conformité aux standards avec **Ruff** :

```bash
# Dans le dossier du service concerné
uv run ruff check .

```

### Tests Unitaires & Couverture

```bash
# Exécution des tests depuis la racine
PYTHONPATH=. uv run pytest --cov=app_api

```

---

## ʕ•ᴥ•ʔっ · · · ✴ Sécurité et Réseau

* **Isolation Réseau** : La base de données est sur un réseau privé (`back-net`), accessible uniquement par le backend.
* **Persistance** : Les données sont sauvegardées dans le volume nommé `postgres_data`, survivant à l'arrêt des conteneurs.
* **CI/CD** : Intégration continue via GitHub Actions pour valider les tests et le formatage à chaque push.

---

## ʕ•ᴥ•ʔっ · · · ✴ Structure des Microservices

```text
.
├── app_api/            # 🧠 Backend (FastAPI, SQLAlchemy, Maths)
├── app_front/          # 🎨 Frontend (Streamlit)
├── tests/              # 🧪 Suite de tests unitaires et conftest
├── docs/               # 📖 Documentation Sphinx
├── docker-compose.yml  # 🏗️ Orchestrateur des services
└── clean_project.sh    # 🧹 Script de maintenance

```