#!/usr/bin/env python3
import sys, json, csv, argparse


def first_point(coords):
    """Recursively find the first [lon, lat] in a nested coords list."""
    if not coords:
        return None, None
    if isinstance(coords[0], (float, int)):
        # coords is [lon, lat]
        return coords[1], coords[0]
    return first_point(coords[0])


def main():
    p = argparse.ArgumentParser(
        description="Convert GeoJSON-Sequence (one Feature per line) to CSV"
    )
    p.add_argument("input", nargs="?", default="data/addresses.jsonl",
                   help="Path to addresses.jsonl (default: data/addresses.jsonl)")
    p.add_argument("output", nargs="?", default="data/addresses.csv",
                   help="Path to output CSV (default: data/addresses.csv)")
    args = p.parse_args()

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
        # optional
        "state",
        "entrance",
        "floor",
        "apartment",
        "building",
        "building_levels",
        "elevator",
        "raw_level",
    ]

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
                # skip lines that aren't valid JSON
                continue

            props = feat.get("properties", {})

            # Required fields
            dp_id = feat.get("id", "")
            country = props.get("addr:country", "")
            county = props.get("addr:county", "")
            muni = props.get("addr:municipality", "")
            city = props.get("addr:city", "")
            zipcode = props.get("addr:postcode", "")
            street = props.get("addr:street", "")
            number = props.get("addr:housenumber", "")

            # Geometry
            geom = feat.get("geometry", {}).get("coordinates", [])
            lat, lon = first_point(geom)
            if lat is None or lon is None:
                # skip objects without valid coordinates
                continue

            # Optional fields
            # Try both "entrance" and "addr:entrance"
            entrance = props.get("entrance", props.get("addr:entrance", ""))

            # Some data might store floors as "level" or "addr:floor"
            floor = props.get("addr:floor", "")
            raw_level = props.get("level", "")  # if you want to see "level" tag

            # Some data uses "building" or "addr:building"; "building:levels" for floors above ground
            building = props.get("building", props.get("addr:building", ""))
            building_levels = props.get("building:levels", "")

            # “apartment” can appear as “addr:unit” or “addr:apartment”; adapt to your data:
            apartment = props.get("addr:apartment", props.get("addr:unit", ""))

            # “elevator”: OSM data might not have a standard key,
            # but if you added nwr/elevator to your filter, you can catch props.get("elevator",""):
            elevator = props.get("elevator", "")

            row = [
                dp_id,
                country,
                county,
                muni,
                city,
                zipcode,
                street,
                number,
                lat,
                lon,
                props.get("addr:state", ""),  # state
                entrance,
                floor,
                apartment,
                building,
                building_levels,
                elevator,
                raw_level,
            ]
            writer.writerow(row)

    print(f"✅ Wrote CSV to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
