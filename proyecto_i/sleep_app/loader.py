"""Carga del dataset de sueño (bedtime_screentime_sleep_debt.csv)."""

from pathlib import Path

import pandas as pd


class DataLoadError(Exception):
    """No se ha podido leer el fichero de entrada."""


def load(path: Path) -> pd.DataFrame:
    """Lee el csv del dataset de sueño.

    Lanza DataLoadError si el fichero no existe, no es un csv o está vacío.
    """
    if not path.exists():
        raise DataLoadError(f"No existe el fichero: {path}")
    if path.suffix.lower() != ".csv":
        raise DataLoadError(f"Solo se aceptan ficheros .csv: {path}")
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError as e:
        raise DataLoadError(f"El fichero está vacío: {path}") from e
