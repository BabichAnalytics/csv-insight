# CSV Insight
Requires Python 3.10 or newer. No extra packages are needed.

```bash
python csv_insight.py sample.csv
python csv_insight.py sample.csv --output report.json
```

On Windows, use `py` instead of `python` if needed.

Reports row and column counts, extra exact duplicate rows, blank or whitespace-only fields, distinct nonempty values, and min/max/mean/median for columns whose nonempty values are all finite numbers. Text such as NA is data, not missing. Numeric-looking IDs are summarized as numbers. Files are processed locally.

Headers must be unique and nonempty; records must have consistent field counts. Empty lines are skipped. The synthetic sample has four rows, one extra duplicate, one missing cost, and one missing days value.

Run tests: `python -m unittest discover -v`.

