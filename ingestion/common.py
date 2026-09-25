"""
Utilitaires partagés par les scripts d'ingestion. `get_connection` est fourni tel quel ;
`fetch_csv` est à vous d'implémenter (cf. TODO)
"""
import os

import duckdb
import pandas as pd
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRONZE_DIR = os.path.join(BASE_DIR, "bronze")
DB_PATH = os.path.join(BASE_DIR, "warehouse.duckdb")
RAW_BASE = "https://raw.githubusercontent.com/kevinl75/tp-polytech-dataset/main"


def fetch_csv(subdir: str, filename: str) -> pd.DataFrame:
    """Doit renvoyer le contenu de <subdir>/<filename> sous forme de DataFrame pandas."""
    # TODO : le fichier CSV source est disponible à l'URL f"{RAW_BASE}/{subdir}/{filename}".
    # - S'il n'existe pas déjà en local dans BRONZE_DIR/<subdir>/<filename>, téléchargez-le et
    #   écrivez-le tel quel sur disque à cet emplacement (créez les dossiers nécessaires).
    # - Eviter si possible de le retéléchargez s'il est déjà présent.

    local_dir = os.path.join(BRONZE_DIR, subdir)
    local_path = os.path.join(local_dir, filename)

    if not os.path.exists(local_path):
        os.makedirs(local_dir, exist_ok=True)
        url = f"{RAW_BASE}/{subdir}/{filename}"

        with urllib.request.urlopen(url) as response:
            raw_bytes = response.read()

        with open(local_path, "wb") as f:
            f.write(raw_bytes)

    return pd.read_csv(local_path)


def get_connection() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(DB_PATH)
