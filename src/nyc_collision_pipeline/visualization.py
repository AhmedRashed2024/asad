"""Visualization helpers for the NYC collision pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd


plt.style.use("seaborn-v0_8")


class VisualizationError(RuntimeError):
    """Raised when a visualization cannot be produced."""


PlotResult = tuple[str, Path]


def _validate_columns(df: pd.DataFrame, required: Iterable[str]) -> None:
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise VisualizationError(f"Missing required columns: {', '.join(missing)}")


def plot_crashes_by_borough(counts: pd.DataFrame, output_dir: Path) -> PlotResult:
    _validate_columns(counts, ["borough", "month", "crash_count"])
    output_path = output_dir / "crashes_by_borough.png"
    pivot = counts.pivot(index="month", columns="borough", values="crash_count").fillna(0)
    pivot.plot(kind="line", figsize=(10, 6))
    plt.title("Monthly NYC Crashes by Borough")
    plt.xlabel("Month")
    plt.ylabel("Number of Crashes")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return "Monthly crash counts by borough", output_path


def plot_injuries_by_vehicle(injuries: pd.DataFrame, output_dir: Path) -> PlotResult:
    _validate_columns(injuries, ["vehicle_type_code1", "persons_injured"])
    output_path = output_dir / "injuries_by_vehicle_type.png"
    top = injuries.head(10).set_index("vehicle_type_code1")
    top["persons_injured"].plot(kind="bar", figsize=(10, 6))
    plt.title("Injuries by Vehicle Type (Top 10)")
    plt.xlabel("Vehicle Type")
    plt.ylabel("Number of Injured Persons")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return "Top vehicle types by injuries", output_path


def create_visualizations(
    *,
    crash_counts: pd.DataFrame,
    vehicle_injuries: pd.DataFrame,
    output_dir: Path,
) -> list[PlotResult]:
    """Create visualizations and return their descriptions and paths."""

    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[PlotResult] = []
    results.append(plot_crashes_by_borough(crash_counts, output_dir))
    results.append(plot_injuries_by_vehicle(vehicle_injuries, output_dir))
    return results


__all__ = [
    "create_visualizations",
    "VisualizationError",
]

