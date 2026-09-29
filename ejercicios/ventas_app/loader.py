from pathlib import Path
from typing import Protocol

import pandas as pd


class DataLoadError(Exception):
    pass


class SalesRepository(Protocol):
    def load(self) -> pd.DataFrame: ...


class CsvSalesRepository:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> pd.DataFrame:
        if not self.path.exists():
            raise DataLoadError(f"No existe el fichero: {self.path}")
        return pd.read_csv(self.path)


class JsonSalesRepository:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> pd.DataFrame:
        if not self.path.exists():
            raise DataLoadError(f"No existe el fichero: {self.path}")
        return pd.read_json(self.path)


def load(path: Path) -> pd.DataFrame:
    repo: SalesRepository
    if path.suffix == ".json":
        repo = JsonSalesRepository(path)
    else:
        repo = CsvSalesRepository(path)
    return repo.load()
