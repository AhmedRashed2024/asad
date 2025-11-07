"""Functions to integrate cleaned collision datasets."""

from __future__ import annotations

import pandas as pd


def integrate_datasets(
    crashes: pd.DataFrame,
    vehicles: pd.DataFrame,
    persons: pd.DataFrame,
) -> pd.DataFrame:
    """Integrate the crashes, vehicles, and persons datasets.

    The resulting frame contains one row per person per vehicle with joined crash details.
    """

    crash_cols = [
        "collision_id",
        "crash_ts",
        "borough",
        "on_street_name",
        "number_of_persons_injured",
        "number_of_persons_killed",
        "number_of_pedestrians_injured",
        "number_of_cyclist_injured",
        "number_of_motorist_injured",
    ]
    vehicle_cols = [
        "collision_id",
        "vehicle_id",
        "vehicle_type_code1",
        "contributing_factor_vehicle_1",
    ]
    person_cols = [
        "collision_id",
        "person_id",
        "person_type",
        "person_injury",
    ]

    crashes_subset = crashes[[col for col in crash_cols if col in crashes.columns]]
    vehicles_subset = vehicles[[col for col in vehicle_cols if col in vehicles.columns]]
    persons_subset = persons[[col for col in person_cols if col in persons.columns]]

    crash_vehicle = pd.merge(vehicles_subset, crashes_subset, on="collision_id", how="left")
    integrated = pd.merge(persons_subset, crash_vehicle, on="collision_id", how="left", suffixes=("_person", "_vehicle"))

    return integrated


__all__ = ["integrate_datasets"]

