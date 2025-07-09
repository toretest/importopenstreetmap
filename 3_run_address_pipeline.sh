#!/usr/bin/env bash
set -euo pipefail

echo "🔍 Filtering for all addr:* and building tags…"
osmium tags-filter data/norway-latest.osm.pbf \
  nwr/addr:country \
  nwr/addr:county \
  nwr/addr:municipality \
  nwr/addr:city \
  nwr/addr:postcode \
  nwr/addr:street \
  nwr/addr:place \
  nwr/addr:suburb \
  nwr/addr:hamlet \
  nwr/addr:village \
  nwr/addr:housenumber \
  nwr/addr:unit \
  nwr/addr:block \
  nwr/addr:floor \
  nwr/building \
  nwr/building:levels \
  nwr/building:use \
  nwr/roof:levels \
  nwr/level \
  nwr/entrance \
  nwr/highway=elevator \
  nwr/source \
  -o data/filtered.osm.pbf \
  --overwrite

echo "📤 Exporting to GeoJSON-Sequence…"
osmium export data/filtered.osm.pbf \
  --output-format=geojsonseq \
  -o data/addresses.jsonl  --overwrite

echo "✅ Done! Now run your Kotlin converter on data/addresses.jsonl"
