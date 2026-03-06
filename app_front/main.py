"""Interface Utilisateur Streamlit - Toolbox IA ʕ•ᴥ•ʔ."""

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
    """Exécute l'interface Streamlit avec monitoring Loguru."""
    st.set_page_config(page_title="Toolbox IA", page_icon="ʕ•ᴥ•ʔ")
    st.title("Toolbox IA - Interface")

    # --- Calculateur ---
    st.header("Calculateur Magique")
    a = st.number_input("Nombre A", value=0.0)
    b = st.number_input("Nombre B", value=0.0)

    if st.button("Calculer"):
        logger.info(f"Utilisateur demande calcul : {a} + {b}")
        try:
            res = requests.get(
                f"{API_URL}/compute/add", params={"a": a, "b": b}, timeout=5
            )
            if res.status_code == 200:
                resultat = res.json().get("result")
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
