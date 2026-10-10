"""Inspect CSV data locally with the Python standard library."""
import argparse
import csv
import json
import math
import statistics
from pathlib import Path

def analyze(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as source:
        reader = csv.reader(source)
        headers = next(reader, None)
        if not headers or any(not h.strip() for h in headers):
            raise ValueError("Every column needs a nonempty header.")
        if len(set(headers)) != len(headers):
            raise ValueError("Duplicate headers are not supported.")
        rows = []
        for line, row in enumerate(reader, 2):
            if not row:
                continue
            if len(row) != len(headers):
                raise ValueError(f"Record {line}: expected {len(headers)} fields, got {len(row)}.")
            rows.append(row)
    columns = {}
    for i, name in enumerate(headers):
        values = [r[i].strip() for r in rows]
        present = [v for v in values if v]
        summary = {"missing": len(values)-len(present), "distinct_nonempty": len(set(present))}
        numbers = []
        for value in present:
            try:
                number = float(value)
            except ValueError:
                break
            if not math.isfinite(number):
                break
            numbers.append(number)
        else:
            if numbers:
                summary["numeric"] = {"count": len(numbers), "min": min(numbers), "max": max(numbers), "mean": statistics.mean(numbers), "median": statistics.median(numbers)}
        columns[name] = summary
    return {"rows": len(rows), "column_count": len(headers), "duplicate_rows": len(rows)-len(set(map(tuple, rows))), "columns": columns}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    try:
        report = json.dumps(analyze(args.csv_file), indent=2, allow_nan=False)
        if args.output:
            if args.output.resolve() == args.csv_file.resolve():
                raise ValueError("Output must differ from input.")
            args.output.write_text(report+"\n", encoding="utf-8")
        print(report)
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        parser.exit(1, f"Error: {error}\n")

if __name__ == "__main__":
    main()

