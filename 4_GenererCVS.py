#!/usr/bin/env python3
import os
import json
import csv
import argparse
from collections import Counter

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def first_point(coords):
    if not coords:
        return None, None
    if isinstance(coords[0], (float, int)):
        return coords[1], coords[0]
    return first_point(coords[0])

def main():
    p = argparse.ArgumentParser(description="Dump raw GeoJSON-Sequence to CSV for further analysis")
    p.add_argument("input", nargs="?", default="data/addresses.jsonl")
    p.add_argument("output", nargs="?", default="data/addresses.csv")
    args = p.parse_args()

    output_dir = "data/out/"
    ensure_dir(output_dir)

    header = [
        "delivery_point_id",
        "country_code", "county", "municipality", "city", "zip_code",
        "street_name", "street_number", "place", "suburb", "hamlet", "village",
        "unit", "block", "floor",
        "lat", "lon",
        "building", "building_levels", "roof_levels", "level", "entrance", "elevator", "building_use"
    ]

    stats = Counter()
    total_rows = 0
    full_address_with_metrics = 0

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
            total_rows += 1
            osm_id = feat.get("id", "")

            def get_val(key):
                val = props.get(key, "").strip()
                if val:
                    stats[key] += 1
                return val

            # Address parts
            country = get_val("addr:country")
            county = get_val("addr:county")
            muni = get_val("addr:municipality")
            city = get_val("addr:city")
            hamlet = get_val("addr:hamlet")
            village = get_val("addr:village")
            suburb = get_val("addr:suburb")
            place = get_val("addr:place")
            zipcode = get_val("addr:postcode")
            street = get_val("addr:street")
            number = get_val("addr:housenumber")
            unit = get_val("addr:unit")
            block = get_val("addr:block")
            floor = get_val("addr:floor")

            lat, lon = first_point(feat.get("geometry", {}).get("coordinates", []))
            if lat is not None and lon is not None:
                stats["coordinates"] += 1

            # Building
            building = get_val("building")
            building_levels = get_val("building:levels")
            roof_levels = get_val("roof:levels")
            level = get_val("level")
            entrance = get_val("entrance")
            building_use = get_val("building:use")

            elevator = get_val("elevator")
            if not elevator and props.get("highway", "") == "elevator":
                elevator = "yes"
                stats["elevator"] += 1

            # Check for full address with metrics
            has_coords = lat is not None and lon is not None
            has_street_address = street and number and city and zipcode and country
            has_place_address = place and number and city and zipcode and country
            has_metrics = building or building_levels or roof_levels or level or entrance or elevator
            if has_coords and (has_street_address or has_place_address) and has_metrics:
                full_address_with_metrics += 1

            row = [
                osm_id,
                country, county, muni, city, zipcode,
                street, number, place, suburb, hamlet, village,
                unit, block, floor,
                lat, lon,
                building, building_levels, roof_levels, level, entrance, elevator, building_use
            ]
            writer.writerow(row)

    print("✅ Raw address export completed.")
    print(f"Total features processed: {total_rows}")
    print("===== FIELD STATISTICS =====")
    for field in sorted(stats.keys()):
        print(f"{field:20}: {stats[field]}")
    print("============================")
    print(f"Addresses with full address and metric information: {full_address_with_metrics}")

if __name__ == "__main__":
    main()
