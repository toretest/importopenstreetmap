#!/usr/bin/env python3
import sys, argparse, json, csv, hashlib

def compute_centroid(coords):
    # Flatten nested coordinate lists and average
    pts = []
    def collect(o):
        if not o: return
        if isinstance(o[0], (int, float)):
            pts.append(o)
        else:
            for sub in o:
                collect(sub)
    collect(coords)
    if not pts:
        return None, None
    lon = sum(p[0] for p in pts)/len(pts)
    lat = sum(p[1] for p in pts)/len(pts)
    return lat, lon

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv",   required=True, help="Output CSV path")
    parser.add_argument("--count", required=True, help="Count file path")
    args = parser.parse_args()

    count = 0
    with open(args.csv, "w", newline="") as outf:
        writer = csv.writer(outf)
        writer.writerow(["uid","postcode","street","housenumber","lat","lon"])
        for raw in sys.stdin:
            line = raw.strip()
            if not line:
                continue
            try:
                feat = json.loads(line)
            except json.JSONDecodeError:
                continue
            props = feat.get("properties", {})
            street  = props.get("addr:street", "")
            number  = props.get("addr:housenumber", "")
            postcode= props.get("addr:postcode", "")

            geom = feat.get("geometry", {}).get("coordinates", [])
            lat, lon = compute_centroid(geom)
            if lat is None or lon is None:
                continue

            key = f"{street}|{number}|{postcode}|{lat}|{lon}"
            uid = hashlib.md5(key.encode()).hexdigest()
            writer.writerow([uid, postcode, street, number, lat, lon])
            count += 1

    with open(args.count, "w") as cf:
        cf.write(str(count))

    print(f"Processed {count} records.", file=sys.stderr)

if __name__ == "__main__":
    main()
