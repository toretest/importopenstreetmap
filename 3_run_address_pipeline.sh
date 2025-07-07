#!/usr/bin/env bash
set -euo pipefail

echo "🔍 Filtering for all addr:* tags…"
#osmium tags-filter data/norway-latest.osm.pbf \
#  nwr/addr:country \
#  nwr/addr:county \
#  nwr/addr:municipality \
#  nwr/addr:city \
#  nwr/addr:postcode \
#  nwr/addr:street \
#  nwr/addr:housenumber \
#  nwr/building \
#  nwr/building:levels \
#  nwr/entrance \
#  nwr/level \
#  nwr/addr:unit \
#  -o data/filtered.osm.pbf \
#  --overwrite

  osmium tags-filter data/norway-latest.osm.pbf \
    nwr/addr:country \
    nwr/addr:county \
    nwr/addr:municipality \
    nwr/addr:city \
    nwr/addr:postcode \
    nwr/addr:street \
    nwr/addr:housenumber \
    nwr/building \
    nwr/building:levels \
    nwr/roof:levels \
    nwr/entrance \
    nwr/level \
    nwr/addr:unit \
    -o data/filtered.osm.pbf \
    --overwrite



echo "📤 Exporting to GeoJSON-Sequence…"
osmium export data/filtered.osm.pbf \
  --output-format=geojsonseq \
  -o data/addresses.jsonl  --overwrite

echo "✅ Done! Now run your Kotlin converter on data/addresses.jsonl"
