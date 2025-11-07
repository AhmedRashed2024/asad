"""Configuration for NYC collision data pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


BASE_URL = "https://data.cityofnewyork.us/resource"


@dataclass(frozen=True)
class DatasetConfig:
    """Configuration for a single dataset."""

    resource_id: str
    filename: str
    description: str
    limit: int = 5000

    def url(self, limit: int | None = None) -> str:
        """Return the CSV download URL for the dataset."""

        effective_limit = limit if limit is not None else self.limit
        return f"{BASE_URL}/{self.resource_id}.csv?$limit={effective_limit}"

    def cache_path(self, directory: Path) -> Path:
        """Return a path suitable for caching the dataset."""

        return directory / self.filename


DATASETS = {
    "crashes": DatasetConfig(
        resource_id="h9gi-nx95",
        filename="mv_collisions_crashes.csv",
        description="NYC Motor Vehicle Collisions - Crashes",
    ),
    "vehicles": DatasetConfig(
        resource_id="bvix-nt5m",
        filename="mv_collisions_vehicles.csv",
        description="NYC Motor Vehicle Collisions - Vehicles",
    ),
    "persons": DatasetConfig(
        resource_id="f55k-p6yu",
        filename="mv_collisions_persons.csv",
        description="NYC Motor Vehicle Collisions - Persons",
    ),
}


DEFAULT_CACHE_DIR = Path("data/raw")

