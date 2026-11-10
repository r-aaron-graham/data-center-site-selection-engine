# Data center site selection engine

A CLI that scores illustrative candidate sites using power, water, land cost,
fiber latency, incentives, and a supplied risk score. It normalizes each
criterion across the input candidates and applies weights in `model.py`.
Higher power, water, and incentives increase the score. Higher cost, latency,
and risk reduce it.

## Run the example

```bash
python -m pip install -r requirements.txt
python model.py --input data/sites.csv --output scores.csv
```

`scores.csv` preserves the input rows and adds the score. Scores are relative
to the supplied candidate set, so adding sites can change existing scores.
The sample values are illustrative. A real site decision requires validated
inputs and engineering due diligence.

Input columns are `site_name`, `power_mw`, `water_million_gallons`,
`land_cost_per_acre`, `fiber_latency_ms`, `tax_incentive_pct`, and `risk_score`.
An empty CSV or nonfinite metric produces an error before output is written.

## Verify

```bash
python -m pip install pytest
python -m pytest -q
```
