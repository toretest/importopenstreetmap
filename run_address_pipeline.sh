#!/usr/bin/env bash
set -euo pipefail

START=$(date +%s)

# 1. Download the Norway extract
echo "⬇️  Downloading Norway OSM PBF…"
mkdir -p data
curl -L https://download.geofabrik.de/europe/norway-latest.osm.pbf \
                -o data/norway-latest.osm.pbf

# 2. Filter to address-tagged ways/nodes
echo "🔍 Filtering for addr:postcode…"
osmium tags-filter data/norway-latest.osm.pbf \
    w/addr:postcode n/addr:postcode \
                           -o data/filtered.osm.pbf

# 3. Export to line-delimited JSON
echo "📤 Exporting to JSON…"
osmium export data/filtered.osm.pbf -f json -o - \
                                       | python3 process_addresses.py \
                                                 --output data/addresses.csv \
                                                          --count-file data/count.txt

END=$(date +%s)
DUR=$((END-START))

echo "✅ Done in ${DUR}s"
echo "• addresses.csv → data/addresses.csv"
echo "• total count → data/count.txt"
