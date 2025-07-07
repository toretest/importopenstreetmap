#!/usr/bin/env bash


echo "🔍 Filtering for addr:postcode (overwrite existing)…"
osmium tags-filter data/norway-latest.osm.pbf \
    w/addr:postcode n/addr:postcode \
                           -o data/filtered.osm.pbf \
                              --overwrite