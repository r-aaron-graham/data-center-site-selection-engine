# Data Center Site Selection Engine

This repository implements a simple scoring engine to evaluate potential
sites for building or expanding data centers.  Each candidate site is
scored on criteria such as power availability, water access, land cost,
fiber connectivity, government incentives, and risk factors (e.g.
seismic, flood).  The aggregated score can be used to rank locations
for further due diligence.

## Usage

Install the required dependencies and run the scoring script on a CSV
file containing site metrics:

```bash
pip install -r requirements.txt
python model.py --input data/sites.csv --output scores.csv
```

The input CSV must include columns: `site_name`, `power_mw`,
`water_million_gallons`, `land_cost_per_acre`, `fiber_latency_ms`,
`tax_incentive_pct`, `risk_score`.  The script computes a normalized
score for each site and writes the results to `scores.csv`.

## Extending

Adjust the weights in `model.py` to reflect your priorities.  For
example, if water is scarce, increase its weight relative to other
factors.  You can also add new criteria by extending the `Site` data
class and updating the scoring logic.