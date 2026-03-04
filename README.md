# IA Foundation Toolbox de Anna

![CI Status](https://github.com/AnnaVitry/Toolbox_IA_de_Anna/actions/workflows/ci.yml/badge.svg)
![Coverage](https://github.com/AnnaVitry/Toolbox_IA_de_Anna/coverage.svg)
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)


Ce projet est un template professionnel standardisé pour le cursus IA. Il intègre la gestion des dépendances avec `uv`, la qualité de code avec `ruff`, les tests avec `pytest` et la documentation automatique avec `Sphinx`.

---

## ʕ•ᴥ•ʔっ · · · ✴ Installation Rapide

Assurez-vous d'avoir [uv](https://github.com/astral-sh/uv) installé.

```bash
git clone [https://github.com/USER/REPO.git](https://github.com/USER/REPO.git)
cd REPO
uv sync
```

### 3. Initialisation de Sphinx

Configurez le moteur de documentation dans le dossier `docs` :

```bash
uv run sphinx-quickstart docs

```

*Réponses recommandées :*

* Separate source and build directories : **y**
* Project name : **IA Foundation Toolbox**
* Author name : **Votre Nom**
* Language : **fr** (ou en)

---

## ʕ•ᴥ•ʔっ · · · ✴ Commandes de Maintenance

Utilisez ces commandes au quotidien pour garantir l'excellence technique du projet.

### Qualité du Code (Linting)

Vérifiez la conformité aux standards Google et corrigez les erreurs de formatage :

```bash
uv run ruff check .        # Analyse
uv run ruff check . --fix  # Correction automatique

```

### Tests Unitaires

Exécutez la suite de tests et vérifiez la couverture de code :

```bash
uv run pytest

```

### Génération de la Documentation

Construisez le site web de documentation en local (format HTML) :

```bash
uv run sphinx-build docs/source public

```

*Le résultat sera disponible dans le dossier `public/index.html`.*

---

## ʕ•ᴥ•ʔっ · · · ✴ Conteneurisation (Docker)

Pour tester l'application dans un environnement reproductible :

```bash
# Construction de l'image
docker build -t ia-toolbox .

# Exécution du conteneur
docker run --rm ia-toolbox

```

---

## ʕ•ᴥ•ʔっ · · · ✴ Intégration Continue (CI)

Le fichier `.github/workflows/ci.yml` automatise ces vérifications à chaque **Push** sur les branches `main` ou `dev`.

* Si un test échoue ou si Ruff détecte une erreur, le déploiement est bloqué.

---

## ʕ•ᴥ•ʔっ · · · ✴ Déploiement en une ligne

Pour valider la qualité, lancer les tests, générer la doc et builder l'image Docker d'un coup :

```bash
./deploy.sh
```