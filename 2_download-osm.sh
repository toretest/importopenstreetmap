#!/usr/bin/env bash

# 1. Download the Norway extract
echo "⬇️  Downloading Norway OSM PBF…"
mkdir -p data
curl -L https://download.geofabrik.de/europe/norway-latest.osm.pbf \
                -o data/norway-latest.osm.pbf