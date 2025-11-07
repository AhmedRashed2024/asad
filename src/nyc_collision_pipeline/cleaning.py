"""Cleaning utilities for NYC collision datasets."""

from __future__ import annotations

import pandas as pd

DATE_COLUMNS = ["crash_date", "crash_time"]


def _parse_datetime(df: pd.DataFrame) -> pd.DataFrame:
    if "crash_date" in df.columns:
        df["crash_date"] = pd.to_datetime(df["crash_date"], errors="coerce")
    if "crash_time" in df.columns:
        df["crash_time"] = pd.to_timedelta(df["crash_time"], errors="coerce")
    if set(DATE_COLUMNS).issubset(df.columns):
        df["crash_ts"] = df["crash_date"] + df["crash_time"]
    return df


def _standardize_borough(df: pd.DataFrame) -> pd.DataFrame:
    if "borough" in df.columns:
        df["borough"] = df["borough"].str.title().fillna("Unknown")
    return df


def clean_crashes(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the crashes dataset."""

    df = df.copy()
    df = _parse_datetime(df)
    df = _standardize_borough(df)
    numeric_columns = [
        "number_of_persons_injured",
        "number_of_persons_killed",
        "number_of_pedestrians_injured",
        "number_of_pedestrians_killed",
        "number_of_cyclist_injured",
        "number_of_cyclist_killed",
        "number_of_motorist_injured",
        "number_of_motorist_killed",
    ]
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0).astype(int)
    df = df.drop_duplicates(subset="collision_id")
    return df


def clean_vehicles(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "vehicle_type_code1" in df.columns:
        df["vehicle_type_code1"] = df["vehicle_type_code1"].str.title()
    df = df.drop_duplicates(subset=["collision_id", "vehicle_id"])
    return df


def clean_persons(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "person_type" in df.columns:
        df["person_type"] = df["person_type"].str.title()
    if "person_injury" in df.columns:
        df["person_injury"] = df["person_injury"].str.title()
    df = df.drop_duplicates(subset=["collision_id", "person_id"])
    return df


__all__ = ["clean_crashes", "clean_vehicles", "clean_persons"]

