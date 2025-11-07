"""Tools for working with NYC Motor Vehicle Collision datasets."""

from .config import DATASETS
from .loader import load_dataset
from .cleaning import clean_crashes, clean_persons, clean_vehicles
from .integration import integrate_datasets
from .analysis import (
    aggregate_crash_counts,
    aggregate_injuries_by_vehicle,
    aggregate_injuries_by_person_role,
)
from .visualization import create_visualizations

__all__ = [
    "DATASETS",
    "load_dataset",
    "clean_crashes",
    "clean_persons",
    "clean_vehicles",
    "integrate_datasets",
    "aggregate_crash_counts",
    "aggregate_injuries_by_vehicle",
    "aggregate_injuries_by_person_role",
    "create_visualizations",
]
