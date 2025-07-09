#!/usr/bin/env python3
import csv
import argparse


def is_deliverable(row):
    """Return True if address is complete (regardless of building type)."""
    return row.get("is_full_address", "").strip().lower() == "true"


def main():
    parser = argparse.ArgumentParser(description="Filter only complete address rows.")
    parser.add_argument("input", nargs="?", default="data/addresses.csv", help="Input CSV file")
    parser.add_argument("output", nargs="?", default="data/addresses_deliverable.csv", help="Output CSV file")
    args = parser.parse_args()

    total_rows = 0
    deliverable_rows = 0

    with open(args.input, "r", encoding="utf-8") as infile, \
            open(args.output, "w", encoding="utf-8", newline="") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        if not fieldnames:
            print("❌ Error: Input file has no headers.")
            return

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            total_rows += 1
            if is_deliverable(row):
                writer.writerow(row)
                deliverable_rows += 1

    print("✅ Filtering complete.")
    print(f"Total rows in input: {total_rows}")
    print(f"Deliverable addresses written: {deliverable_rows}")
    print(f"Output file: {args.output}")


if __name__ == "__main__":
    main()
