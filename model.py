"""Site selection engine for data centers.

Reads site metrics from a CSV file, normalizes them, applies weights to
compute an overall score, and writes the results to an output file.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List

import click
import numpy as np


@dataclass
class Site:
    name: str
    power_mw: float
    water_million_gallons: float
    land_cost_per_acre: float
    fiber_latency_ms: float
    tax_incentive_pct: float
    risk_score: float
    score: float | None = None


def normalize(values: List[float]) -> List[float]:
    arr = np.array(values, dtype=float)
    min_val, max_val = arr.min(), arr.max()
    if max_val == min_val:
        return [0.0 for _ in values]
    return ((arr - min_val) / (max_val - min_val)).tolist()


def compute_scores(sites: List[Site]) -> List[Site]:
    # Normalize each criterion.  For cost and latency, lower is better, so invert later.
    power_norm = normalize([s.power_mw for s in sites])
    water_norm = normalize([s.water_million_gallons for s in sites])
    land_norm = normalize([s.land_cost_per_acre for s in sites])
    latency_norm = normalize([s.fiber_latency_ms for s in sites])
    tax_norm = normalize([s.tax_incentive_pct for s in sites])
    risk_norm = normalize([s.risk_score for s in sites])
    # Weights reflect relative importance.  Adjust as needed.
    weights = {
        "power": 0.25,
        "water": 0.2,
        "land": 0.15,
        "latency": 0.15,
        "tax": 0.15,
        "risk": 0.1,
    }
    for i, site in enumerate(sites):
        # Higher power, water, tax incentive are better; lower cost, latency, risk are better.
        score = (
            weights["power"] * power_norm[i]
            + weights["water"] * water_norm[i]
            + weights["tax"] * tax_norm[i]
            + weights["land"] * (1 - land_norm[i])
            + weights["latency"] * (1 - latency_norm[i])
            + weights["risk"] * (1 - risk_norm[i])
        )
        site.score = round(float(score), 4)
    return sites


@click.command()
@click.option(
    "--input",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
    help="Path to CSV file with site metrics.",
)
@click.option(
    "--output",
    type=click.Path(dir_okay=False, path_type=Path),
    required=True,
    help="Path to write output CSV with scores.",
)
def main(input: Path, output: Path):
    """Compute site selection scores."""
    sites: List[Site] = []
    with input.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            site = Site(
                name=row["site_name"],
                power_mw=float(row["power_mw"]),
                water_million_gallons=float(row["water_million_gallons"]),
                land_cost_per_acre=float(row["land_cost_per_acre"]),
                fiber_latency_ms=float(row["fiber_latency_ms"]),
                tax_incentive_pct=float(row["tax_incentive_pct"]),
                risk_score=float(row["risk_score"]),
            )
            sites.append(site)
    compute_scores(sites)
    with output.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "site_name",
            "power_mw",
            "water_million_gallons",
            "land_cost_per_acre",
            "fiber_latency_ms",
            "tax_incentive_pct",
            "risk_score",
            "score",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in sites:
            writer.writerow(
                {
                    "site_name": s.name,
                    "power_mw": s.power_mw,
                    "water_million_gallons": s.water_million_gallons,
                    "land_cost_per_acre": s.land_cost_per_acre,
                    "fiber_latency_ms": s.fiber_latency_ms,
                    "tax_incentive_pct": s.tax_incentive_pct,
                    "risk_score": s.risk_score,
                    "score": s.score,
                }
            )
    click.echo(f"Wrote scores for {len(sites)} sites to {output}")


if __name__ == "__main__":  # pragma: no cover
    main()