# doc install 

## Source: openstreetmap import

chmod +x run_address_pipeline.sh

https://download.geofabrik.de/europe/norway.html
curl -L https://download.geofabrik.de/europe/norway-latest.osm.pbf \
-o data/norway-latest.osm.pbf


## 1use python 3.11 frow /opt/homebrew/....
source .venv/bin/activate
pip install --upgrade pip
pip freeze > requirements.txt

mkdir -p src/mymodule
touch src/mymodule/__init__.py
touch src/mymodule/logic.py

touch xxx.py -> Creates an empty file if it doesn’t exist.
             -> Updates the "last modified" time if the file does exist
```bash
PYTHONPATH=src python main.py
```


## Stucture

importopenstreetmap/
├── .venv/                ← virtual environment
├── .git/                 ← Git config
├── .idea/                ← IntelliJ IDEA project files
├── requirements.txt      ← pip dependencies
├── install.md            ← your notes / install instructions
├── main.py               ← entry point (or script)
├── data/norway-latest.osm.pbf ← data files (e.g., OSM data)
├── src/                  ← source code lives here
│   └── importosmmodule/         ← your Python package
│       ├── __init__.py   ← makes this a package 
│       └── logic.py      ← put real logic here
└── tests/                ← optional: tests
└── test_logic.py


* __init__.py
This folder is a package, and you can import from it.
Python may not recognize the folder as a module you can import
t's perfectly valid to leave it empty.
Expose certain functions or classes:


## read osm data M mack Silicon (M1/M2/M4)

### Filter the PBF to only address‐tagged elements

Try docker build and other stuff and endded up with the osmium CLI tool 

```terminal
osmium tags-filter data/norway-latest.osm.pbf w/addr:postcode -o filtered.osm.pbf
```
osmium: the CLI tool you installed via Homebrew

tags-filter: subcommand that scans the input PBF and keeps only those OSM elements matching the tag filter

data/norway-latest.osm.pbf: your full Norway extract

w/addr:postcode: filter expression—keep ways (w) that have an addr:postcode tag

-o filtered.osm.pbf: write the result to a new PBF file containing only those address‐tagged ways

Result: filtered.osm.pbf contains just the subset of buildings (and their nodes) that have a postcode.


### Export the filtered PBF to line‐delimited JSON
```terminal

osmium export filtered.osm.pbf -f json -o addrs.json
```

export: subcommand that converts a PBF into JSON

-f json: output format is line‐delimited JSON (one JSON object per line)

-o addrs.json: write the JSON to addrs.json

Each JSON object includes:

OSM tags (e.g. addr:street, addr:housenumber, addr:postcode)

A centroid field with latitude/longitude

Other metadata you can ignore

### Process that JSON in Python
```python
python main.py data/out/addrs.json
```
