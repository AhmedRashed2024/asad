"""Command-line interface for the NYC collision data pipeline."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

from nyc_collision_pipeline import (
    DATASETS,
    aggregate_crash_counts,
    aggregate_injuries_by_person_role,
    aggregate_injuries_by_vehicle,
    clean_crashes,
    clean_persons,
    clean_vehicles,
    create_visualizations,
    integrate_datasets,
    load_dataset,
)

LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional row limit for each dataset download",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable local caching of datasets",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="Location for cached datasets (defaults to data/raw)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory for generated analysis tables and figures",
    )
    return parser.parse_args()


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run(limit: int | None, use_cache: bool, cache_dir: Path | None, output_dir: Path) -> None:
    configure_logging()
    LOGGER.info("Starting NYC collision pipeline")

    dfs: dict[str, pd.DataFrame] = {}
    for name in DATASETS:
        LOGGER.info("Loading dataset: %s", name)
        dfs[name] = load_dataset(
            name, limit=limit, use_cache=use_cache, cache_dir=cache_dir
        )

    LOGGER.info("Cleaning datasets")
    crashes = clean_crashes(dfs["crashes"])
    vehicles = clean_vehicles(dfs["vehicles"])
    persons = clean_persons(dfs["persons"])

    LOGGER.info("Integrating datasets")
    integrated = integrate_datasets(crashes, vehicles, persons)

    LOGGER.info("Running analyses")
    crash_counts = aggregate_crash_counts(crashes)
    vehicle_injuries = aggregate_injuries_by_vehicle(integrated)
    person_role = aggregate_injuries_by_person_role(integrated)

    output_dir.mkdir(parents=True, exist_ok=True)

    LOGGER.info("Saving analysis tables to %s", output_dir)
    crash_counts.to_csv(output_dir / "crash_counts_by_borough_month.csv", index=False)
    vehicle_injuries.to_csv(output_dir / "injuries_by_vehicle_type.csv", index=False)
    person_role.to_csv(output_dir / "injuries_by_person_role.csv", index=False)

    LOGGER.info("Generating visualizations")
    create_visualizations(
        crash_counts=crash_counts,
        vehicle_injuries=vehicle_injuries,
        output_dir=output_dir,
    )

    LOGGER.info("Pipeline complete")


def main() -> None:
    args = parse_args()
    run(
        limit=args.limit,
        use_cache=not args.no_cache,
        cache_dir=args.cache_dir,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()

