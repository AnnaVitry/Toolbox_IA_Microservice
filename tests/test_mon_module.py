"""Suite de tests pour le module métier.

Ce module valide les calculs mathématiques et la lecture de structures
de données Pandas en utilisant les fonctions de mon_module.py.
"""

import os
import sys

import pandas as pd
import pytest
from app_api.modules.mon_module import add, print_data, square

# Ajoute la racine du projet au chemin de recherche de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Maintenant, l'import fonctionnera
# --- TESTS MATHÉMATIQUES ---


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 5, 15),  # Cas standard
        (-1, 1, 0),  # Nombres négatifs
        (0, 0, 0),  # Zéro
        (2.5, 2.5, 5.0),  # Floats
    ],
)
def test_add(a, b, expected):
    """Vérifie l'addition pour différents types de nombres."""
    assert add(a, b) == expected


def test_square():
    """Vérifie le calcul du carré."""
    assert square(4) == 16
    assert square(-3) == 9  # Un carré est toujours positif


def test_add_wrong_type():
    """Test de robustesse : que se passe-t-il si on passe une chaîne ?."""
    with pytest.raises(TypeError):
        add("1", 2)


# --- TESTS PANDAS ---


@pytest.fixture
def sample_df():
    """Génère un DataFrame de test."""
    return pd.DataFrame({"A": [1, 2, 3], "B": ["a", "b", "c"]})


def test_print_data(sample_df):
    """Vérifie que print_data retourne le bon nombre de lignes."""
    result = print_data(sample_df)
    assert result == 3
    assert isinstance(result, int)


def test_print_data_empty():
    """Vérifie le comportement avec un DataFrame vide."""
    empty_df = pd.DataFrame()
    assert print_data(empty_df) == 0
