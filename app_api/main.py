"""Point d'entrée de l'API FastAPI avec monitoring Loguru."""

import sys
import time

from fastapi import Depends, FastAPI, HTTPException
from loguru import logger
from sqlalchemy.orm import Session

# Imports internes
from app_api.maths.mon_module import add
from app_api.models.database import Base, Calcul
from app_api.modules.connect import engine, get_db

# Configuration de Loguru
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan> - "
    "<level>{message}</level>"
)
logger.remove()
logger.add(
    sys.stdout,
    format=LOG_FORMAT,
    level="INFO",
)

# Création des tables
try:
    Base.metadata.create_all(bind=engine)
    logger.success("Initialisation de la base de données réussie.")
except Exception as e:
    logger.critical(f"Impossible d'initialiser la base de données : {e}")

app = FastAPI(title="Toolbox IA API")


@app.on_event("startup")
def startup():
    """Action au démarrage de l'API (Corrigée pour D103)."""
    logger.info("ʕ•ᴥ•ʔ Microservice API prêt à l'emploi.")


@app.get("/compute/add")
def compute_add(a: float, b: float, db: Session = Depends(get_db)):
    """Calcule l'addition et persiste le résultat avec traçabilité."""
    start_time = time.time()
    logger.info(f"Requête reçue : addition de {a} et {b}")

    try:
        # Calcul
        res = add(a, b)

        # Persistance
        nouveau_calcul = Calcul(a=a, b=b, resultat=res)
        db.add(nouveau_calcul)
        db.commit()

        duration = time.time() - start_time
        logger.success(f"Calcul sauvegardé : {res} (Temps : {duration:.4f}s)")

        return {"result": res, "saved": True, "duration": duration}

    except Exception:
        db.rollback()  # Annule la transaction en cas d'erreur
        logger.exception("Erreur lors du calcul ou de l'enregistrement en base")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@app.get("/data")
def get_history(db: Session = Depends(get_db)):
    """Récupère l'historique avec monitoring de charge."""
    logger.debug("Consultation de l'historique demandée")
    try:
        historique = db.query(Calcul).all()
        logger.info(f"Historique récupéré : {len(historique)} entrées trouvées")
        return historique
    except Exception as e:
        logger.error(f"Échec de la récupération des données : {e}")
        raise HTTPException(status_code=500, detail="Base de données inaccessible")
