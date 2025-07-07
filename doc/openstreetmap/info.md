Below is an example of how you might expand your osmium tags-filter command to extract objects (nodes, ways, and relations) that carry the relevant address/building tags. This keeps any geometry (which means you can later retrieve lat/lon from node objects, or from way/polycentroids if needed).

```terminal
osmium tags-filter data/norway-latest.osm.pbf \
n/addr:country w/addr:country r/addr:country \
n/addr:county w/addr:county r/addr:county \
n/addr:municipality w/addr:municipality r/addr:municipality \
n/addr:city w/addr:city r/addr:city \
n/addr:postcode w/addr:postcode r/addr:postcode \
n/addr:street w/addr:street r/addr:street \
n/addr:housenumber w/addr:housenumber r/addr:housenumber \
n/addr:state w/addr:state r/addr:state \
n/entrance w/entrance r/entrance \
n/addr:floor w/addr:floor r/addr:floor \
n/addr:apartment w/addr:apartment r/addr:apartment \
n/building w/building r/building \
n/elevator w/elevator r/elevator \
-o data/filtered.osm.pbf
```
did not work, so I added the trye

```terminal

osmium tags-filter data/norway-latest.osm.pbf \
  n/addr:country        w/addr:country        r/addr:country        \
  n/addr:county         w/addr:county         r/addr:county         \
  n/addr:municipality   w/addr:municipality   r/addr:municipality   \
  n/addr:city           w/addr:city           r/addr:city           \
  n/addr:postcode       w/addr:postcode       r/addr:postcode       \
  n/addr:street         w/addr:street         r/addr:street         \
  n/addr:housenumber    w/addr:housenumber    r/addr:housenumber    \
  n/addr:state          w/addr:state          r/addr:state          \
  n/addr:entrance       w/addr:entrance       r/addr:entrance       \
  n/addr:floor          w/addr:floor          r/addr:floor          \
  n/addr:apartment      w/addr:apartment      r/addr:apartment      \
  n/addr:building       w/addr:building       r/addr:building       \
  n/addr:elevator       w/addr:elevator       r/addr:elevator       \
  -o data/filtered.osm.pbf \
  --overwrite

```

pip install osmium

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew update
brew install python
python3 --version
alias python='python3'
source ~/.zshrc


You can safely run pip through python3’s built-in module like so:
python3 -m pip install <package_name>

Other 

chmod +x jsonl_to_csv.py
./jsonl_to_csv.py data/addresses.jsonl data/addresses.csv


search
```termina
curl -s 'https://overpass-api.de/api/interpreter' \
--data-urlencode 'data=
[out:json][timeout:25];
area["ISO3166-1"="NO"][admin_level=2]->.nor;
(
node(area.nor)["addr:street"~"[Mm]ovei"];
way(area.nor)["addr:street"~"[Mm]ovei"];
);
out tags center;
' \
| jq .

```

```terminal
curl -s 'https://overpass-api.de/api/interpreter' \
  --data-urlencode 'data=
    [out:json][timeout:25];
    area["ISO3166-1"="NO"][admin_level=2]->.nor;
    (
      node(area.nor)["addr:floor"];
      way(area.nor)["addr:floor"];
      relation(area.nor)["addr:floor"];
      node(area.nor)["addr:building"];
      way(area.nor)["addr:building"];
      relation(area.nor)["addr:building"];
      node(area.nor)["addr:entrance"];
      way(area.nor)["addr:entrance"];
      relation(area.nor)["addr:entrance"];
    );
    out tags center 10;
  ' \
| jq '{
    floor: ( [.elements[] 
      | select(.tags["addr:floor"]!=null) 
      | {id, type, floor: .tags["addr:floor"]} 
    ] | unique ),
    building: ( [.elements[] 
      | select(.tags["addr:building"]!=null) 
      | {id, type, building: .tags["addr:building"]} 
    ] | unique ),
    entrance: ( [.elements[] 
      | select(.tags["addr:entrance"]!=null) 
      | {id, type, entrance: .tags["addr:entrance"]} 
    ] | unique )
  }'

```

result
```json
{
"floor": [],
"building": [],
"entrance": []
}
```

```terminal
grep -i 'Øvre Movei' data/addresses.csv
```

```terminal
for tag in floor building entrance; do
echo -n "$tag: "
osmium tags-filter data/filtered.osm.pbf \
n/addr:$tag w/addr:$tag r/addr:$tag \
-o - --output-format=pbf \
| osmium fileinfo -e - --input-format=pbf \
| awk '/Number of nodes:/ {n=$3} /Number of ways:/ {w=$3} END {print n+w}'
done
```


