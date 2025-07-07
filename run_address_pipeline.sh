#!/usr/bin/env bash
set -euo pipefail

START=$(date +%s)

echo "🔍 Filtering for addr:postcode…"
osmium tags-filter data/norway-latest.osm.pbf \
    n/addr:postcode w/addr:postcode \
    -o data/filtered.osm.pbf \
    --overwrite

echo "📤 Exporting GeoJSON-Sequence and converting to CSV…"
osmium export data/filtered.osm.pbf \
  --output-format=geojsonseq \
  -o - \
  | python3 main.py \
      --csv   data/addresses.csv \
      --count data/count.txt

END=$(date +%s)
echo "✅ Done in $((END-START))s"
echo " • CSV   → data/addresses.csv"
echo " • Count → data/count.txt"
