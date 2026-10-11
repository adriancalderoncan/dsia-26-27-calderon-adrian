"""Carga de los datos de ventas desde fichero (csv o json)."""

from pathlib import Path
from typing import Protocol

import pandas as pd


class DataLoadError(Exception):
    """No se han podido cargar los datos de entrada."""


class SalesRepository(Protocol):
    """Cualquier origen de ventas que sepa devolver un DataFrame con load()."""

    def load(self) -> pd.DataFrame:
        """Devuelve las ventas como DataFrame."""
        ...


class CsvSalesRepository:
    """Lee las ventas de un fichero csv."""

    def __init__(self, path: Path):
        self.path = path

    def load(self) -> pd.DataFrame:
        """Lanza DataLoadError si el fichero no existe."""
        if not self.path.exists():
            raise DataLoadError(f"No existe el fichero: {self.path}")
        return pd.read_csv(self.path)


class JsonSalesRepository:
    """Lee las ventas de un fichero json con una lista de registros."""

    def __init__(self, path: Path):
        self.path = path

    def load(self) -> pd.DataFrame:
        """Lanza DataLoadError si el fichero no existe."""
        if not self.path.exists():
            raise DataLoadError(f"No existe el fichero: {self.path}")
        return pd.read_json(self.path)


def load(path: Path) -> pd.DataFrame:
    """Elige el lector según la extensión del fichero y devuelve los datos.

    Lanza DataLoadError si el fichero no existe.
    """
    repo: SalesRepository
    if path.suffix == ".json":
        repo = JsonSalesRepository(path)
    else:
        repo = CsvSalesRepository(path)
    return repo.load()
