# NYC Motor Vehicle Collisions Pipeline

This repository provides a Python implementation of the project outline shown in the
assignment screenshot. It automates the data engineering workflow for the NYC Motor
Vehicle Collisions datasets by downloading, cleaning, integrating, analyzing, and
visualizing the data directly from NYC Open Data.

## Features

* Download crash, vehicle, and person level datasets from NYC Open Data using the public SODA API.
* Cache downloaded CSV files locally for repeatable runs.
* Clean and standardize the datasets (dates, borough names, numeric columns, and categorical labels).
* Integrate the three datasets into a person-level view joined with crash and vehicle context.
* Produce summary tables for crash counts, vehicle injury totals, and injury outcomes by person role.
* Generate example Matplotlib figures that mirror the milestone 2 visualization goals.

## Project Structure

```
├── data/                # Default cache location for downloaded CSVs
├── outputs/             # Generated tables and figures
├── scripts/
│   └── run_pipeline.py  # Command-line entry point
└── src/nyc_collision_pipeline/
    ├── __init__.py
    ├── analysis.py
    ├── cleaning.py
    ├── config.py
    ├── integration.py
    ├── loader.py
    └── visualization.py
```

## Getting Started

1. Install dependencies (a virtual environment is recommended):

   ```bash
   pip install -r requirements.txt
   ```

2. Run the pipeline. The `--limit` flag controls how many rows are fetched from each
   dataset (the NYC API defaults to 1000 rows if a limit is not provided). A smaller
   limit can be useful while experimenting locally.

   ```bash
   python scripts/run_pipeline.py --limit 2000
   ```

   The command downloads the datasets, performs the cleaning and integration steps,
   writes analysis tables to `outputs/`, and saves illustrative charts in the same
   directory.

3. To refresh the cache or change where files are stored, use the optional flags:

   ```bash
   python scripts/run_pipeline.py --no-cache --cache-dir /tmp/nyc_cache --output-dir reports
   ```

## Extending the Analysis

The modular design makes it straightforward to adapt the pipeline for additional
milestones in the assignment. You can add new aggregation helpers to `analysis.py`,
create more detailed charts in `visualization.py`, or append steps to the main
script to support machine learning tasks or dashboards.

