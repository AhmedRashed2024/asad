"""Analysis helpers for NYC collision data."""

from __future__ import annotations

import pandas as pd


def aggregate_crash_counts(crashes: pd.DataFrame) -> pd.DataFrame:
    """Return crash counts grouped by borough and month."""

    if "crash_ts" not in crashes.columns:
        raise ValueError("crashes dataframe must include 'crash_ts' column")
    temp = crashes.copy()
    temp["month"] = temp["crash_ts"].dt.to_period("M")
    counts = (
        temp.groupby(["borough", "month"], dropna=False)["collision_id"].count().reset_index(name="crash_count")
    )
    return counts.sort_values(["month", "borough"])


def aggregate_injuries_by_vehicle(integrated: pd.DataFrame) -> pd.DataFrame:
    """Aggregate injuries by vehicle type."""

    cols = [
        "vehicle_type_code1",
        "number_of_persons_injured",
        "number_of_persons_killed",
    ]
    available_cols = [col for col in cols if col in integrated.columns]
    temp = integrated[available_cols].copy()
    grouped = (
        temp.groupby("vehicle_type_code1", dropna=False)
        .agg({
            "number_of_persons_injured": "sum",
            "number_of_persons_killed": "sum",
        })
        .reset_index()
        .rename(columns={
            "number_of_persons_injured": "persons_injured",
            "number_of_persons_killed": "persons_killed",
        })
    )
    return grouped.sort_values("persons_injured", ascending=False)


def aggregate_injuries_by_person_role(integrated: pd.DataFrame) -> pd.DataFrame:
    """Aggregate injuries and fatalities by person role."""

    if "person_type" not in integrated.columns or "person_injury" not in integrated.columns:
        raise ValueError("integrated dataframe must include 'person_type' and 'person_injury'")
    pivot = (
        integrated.assign(count=1)
        .pivot_table(
            index="person_type",
            columns="person_injury",
            values="count",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
    )
    return pivot


__all__ = [
    "aggregate_crash_counts",
    "aggregate_injuries_by_vehicle",
    "aggregate_injuries_by_person_role",
]

