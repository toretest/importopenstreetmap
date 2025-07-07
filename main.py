#!/usr/bin/env python3
import os
import json
import csv
import argparse
from collections import Counter


def ensure_dir(directory):
    """Ensure the directory exists, create it if it doesn't."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def first_point(coords):
    """Recursively find the first [lat, lon] in a nested coords list."""
    if not coords:
        return None, None
    if isinstance(coords[0], (float, int)):
        # Coords is in [lon, lat] format, reverse it to [lat, lon]
        return coords[1], coords[0]
    return first_point(coords[0])


def main():
    p = argparse.ArgumentParser(
        description="Convert GeoJSON-Sequence (one Feature per line) to CSV and generate a detailed report."
    )
    p.add_argument("input", nargs="?", default="data/addresses.jsonl",
                   help="Path to addresses.jsonl (default: data/addresses.jsonl)")
    p.add_argument("output", nargs="?", default="data/addresses.csv",
                   help="Path to output CSV (default: data/addresses.csv)")
    args = p.parse_args()

    # Output directories
    output_dir = "data/out/"
    ensure_dir(output_dir)

    # CSV Headers
    header = [
        "delivery_point_id",
        "country_code",
        "county",
        "municipality",
        "city",
        "zip_code",
        "street_name",
        "street_number",
        "lat",
        "lon",
        "full_address",
    ]

    # Initialize counters and collectors
    total_addresses = 0
    problem_entries = []
    missing_entries_count = 0
    optional_fields_stats = Counter()

    # Debugging elevators
    elevator_entries = []  # To log all elevator entries for inspection

    # Open input and output files
    with open(args.input, "r", encoding="utf-8") as inf, \
            open(args.output, "w", encoding="utf-8", newline="") as outf:

        writer = csv.writer(outf)
        writer.writerow(header)

        for raw_line in inf:
            line = raw_line.strip()
            if not line:
                continue

            try:
                feat = json.loads(line)
            except json.JSONDecodeError:
                continue

            props = feat.get("properties", {})
            total_addresses += 1

            # Core fields
            dp_id = feat.get("id", "")
            country = props.get("addr:country", "").strip()
            county = props.get("addr:county", "").strip()
            muni = props.get("addr:municipality", "").strip()
            city = props.get("addr:city", "").strip()
            zipcode = props.get("addr:postcode", "").strip()
            street = props.get("addr:street", "").strip()
            number = props.get("addr:housenumber", "").strip()

            # Geometry
            geom = feat.get("geometry", {}).get("coordinates", [])
            lat, lon = first_point(geom)

            # Full Address Logic
            if street and number and city:
                full_address = f"{street} {number}, {zipcode} {city}, {country}".strip(", ")
            elif lat and lon:
                full_address = f"Coordinates ({lat}, {lon})"
            else:
                full_address = "<Incomplete Address>"

            # Collect optional fields stats for reporting
            for field in ["building", "building:levels", "roof:levels", "elevator"]:
                if props.get(field, "").strip():
                    optional_fields_stats[field] += 1

            # ### FIX: Improve Elevator Detection ###
            # Count any entry with `highway=elevator`
            if props.get("highway", "").strip() == "elevator":
                optional_fields_stats["elevator"] += 1
                elevator_entries.append({"lat": lat, "lon": lon, "properties": props})

            # Collect problematic entries for missing mandatory data
            if not number and not (lat and lon):  # If both are missing
                problem_entries.append({
                    "address": full_address,
                    "lat": lat,
                    "lon": lon
                })
                missing_entries_count += 1

            # Write only critical fields to CSV
            row = [
                dp_id, country, county, muni, city, zipcode, street, number,
                lat, lon, full_address
            ]
            writer.writerow(row)

    # Output debug elevator entries for inspection
    elevator_debug_file = os.path.join(output_dir, "elevator_debug.jsonl")
    with open(elevator_debug_file, "w", encoding="utf-8") as debug_out:
        for entry in elevator_entries:
            json.dump(entry, debug_out)
            debug_out.write("\n")

    # Generate Report
    print("===== REPORT =====")
    print(f"Total addresses processed: {total_addresses}")
    print("\nOptional fields presence statistics:")
    for field, count in optional_fields_stats.items():
        print(f"  - {field}: {count}")  # Display optional field stats

    # Debugging: Show elevator entries detected
    print("\nElevator Debugging Output Written to:", elevator_debug_file)
    print(f"Detected {len(elevator_entries)} elevators!")

    # Report problematic entries
    print("\nProblematic entries (missing address and coordinates):")
    if missing_entries_count == 0:
        print("No problematic entries found (0).")
    else:
        # Print first 10 problematic entries for readability
        for issue in problem_entries[:10]:
            print(f"  - Address: {issue['address']} | Coordinates: ({issue['lat']}, {issue['lon']})")
    print(f"Total problematic entries: {missing_entries_count}")
    print("==================")


if __name__ == "__main__":
    main()