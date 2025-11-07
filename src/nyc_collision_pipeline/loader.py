"""Functions for downloading and caching NYC collision datasets."""

from __future__ import annotations

import io
import logging
from pathlib import Path
from typing import Literal

import pandas as pd
import requests

from .config import DATASETS, DEFAULT_CACHE_DIR, DatasetConfig

LOGGER = logging.getLogger(__name__)


DatasetName = Literal["crashes", "vehicles", "persons"]


def ensure_cache_dir(directory: Path) -> None:
    """Ensure the cache directory exists."""

    directory.mkdir(parents=True, exist_ok=True)


def fetch_dataset(dataset: DatasetConfig, limit: int | None = None) -> pd.DataFrame:
    """Fetch a dataset from NYC Open Data.

    Parameters
    ----------
    dataset:
        Configuration for the dataset to download.
    limit:
        Optional override for the number of rows to download.
    """

    url = dataset.url(limit)
    LOGGER.info("Downloading %s", url)
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text))


def load_dataset(
    name: DatasetName,
    *,
    limit: int | None = None,
    use_cache: bool = True,
    cache_dir: Path | None = None,
) -> pd.DataFrame:
    """Load a dataset with optional caching.

    Parameters
    ----------
    name:
        Name of the dataset (``"crashes"``, ``"vehicles"``, ``"persons"``).
    limit:
        Optional override for number of rows to download.
    use_cache:
        If ``True`` the dataset will be cached on disk.
    cache_dir:
        Optional path to the cache directory; defaults to :data:`DEFAULT_CACHE_DIR`.
    """

    dataset = DATASETS[name]
    cache_dir = cache_dir or DEFAULT_CACHE_DIR
    ensure_cache_dir(cache_dir)
    cache_path = dataset.cache_path(cache_dir)

    if use_cache and cache_path.exists():
        LOGGER.info("Loading %s from cache", cache_path)
        return pd.read_csv(cache_path)

    df = fetch_dataset(dataset, limit=limit)
    if use_cache:
        LOGGER.info("Caching %s to %s", dataset.description, cache_path)
        df.to_csv(cache_path, index=False)
    return df


__all__ = ["load_dataset", "DatasetName"]

