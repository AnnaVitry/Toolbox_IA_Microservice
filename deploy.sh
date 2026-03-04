#!/bin/bash

# Configuration des couleurs
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
CYAN="\033[0;36m"
NC="\033[0m" # No Color (Reset)

# Arrêter le script à la moindre erreur
set -e

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE} DÉMARRAGE DU PIPELINE DE DÉPLOIEMENT ʕ•ᴥ•ʔ${NC}"
echo -e "${BLUE}====================================================${NC}"

echo -e "\n${CYAN}[1/4]${NC} ${YELLOW}Analyse de la qualité du code (Ruff)...${NC}"
uv run ruff check .
echo -e "${GREEN}✔ Qualité validée.${NC}"

echo -e "\n${CYAN}[2/4]${NC} ${YELLOW}Exécution des tests unitaires (Pytest)...${NC}"
uv run pytest
echo -e "${GREEN}✔ Tests réussis.${NC}"

echo -e "\n${CYAN}[3/4]${NC} ${YELLOW}Génération de la documentation (Sphinx)...${NC}"
uv run sphinx-build docs/source public
echo -e "${GREEN}✔ Documentation générée dans le dossier 'public'.${NC}"

echo -e "\n${CYAN}[4/4]${NC} ${YELLOW}Construction de l'image Docker...${NC}"
# Forçage du contexte au besoin : export DOCKER_HOST=unix:///var/run/docker.sock
docker build -t ia-toolbox .
echo -e "${GREEN}✔ Image Docker 'ia-toolbox' créée avec succès.${NC}"

echo -e "\n${BLUE}====================================================${NC}"
echo -e "${GREEN} DÉPLOIEMENT TERMINÉ AVEC SUCCÈS ! ʕ•ᴥ•ʔ${NC}"
echo -e "${BLUE}====================================================${NC}"
echo -e "${YELLOW} Pour lancer le conteneur :${NC} ${CYAN}docker run --rm ia-toolbox${NC}"