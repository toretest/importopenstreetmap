# doc

https://wiki.openstreetmap.org/wiki/Import/Catalogue/Norway_Building_Import
https://github.com/NKAmapper/building2osm

Resultat:

## 4_Generere_filteredCVS.py

===== REPORT =====
Total addresses processed: 16545074
- level: 12057
- entrance: 10096
- building: 8326757
- elevator: 219
- building:levels: 421420
- roof:levels: 41473
  Elevators found: 219
  ==================
- 

## 5_filter_complete_addresses.py:

Total rows in input: 16545074
Deliverable addresses written: 19
Output file: data/addresses_deliverable.csv


Det kan virke som om noen adresser og bygningsdetaljer mangler i ditt utdrag fra norway-latest.osm.pbf. Dette skyldes ikke feil i din osmium-kommando, men heller hvordan adresse- og bygningsdata er strukturert i OpenStreetMap (OSM) for Norge.


🏠 Adresser i Norge: Separate noder
I Norge er adresser importert fra Kartverkets matrikkeldata og lagt inn som separate noder, ikke direkte på bygninger. Dette er en bevisst beslutning fra det norske OSM-fellesskapet for å forenkle vedlikehold og oppdateringer. Derfor vil adresser ofte finnes som egne noder med 

- addr:*-tagger, uavhengig av bygningene de tilhører.

Bygningsdata og detaljer
Bygningsdata i Norge er i stor grad importert fra Kartverkets matrikkel, som gir detaljerte 2D-polygoner og bygningsinformasjon. Imidlertid er det ikke alle bygninger som har komplette detaljer som 

building:levels 
  eller 
roof:levels. 

Dette kan variere avhengig av tilgjengeligheten av data for hver kommune.

Hva du kan gjøre videre

- Sjekk adresse- og bygningsnoder separat: Bruk osmium eller andre verktøy for å filtrere ut noder med addr:*-tagger og bygninger med building=*.
- Bruk JOSM for visuell inspeksjon: JOSM-editoren lar deg laste inn og inspisere data visuelt, noe som kan hjelpe deg med å identifisere manglende eller ufullstendige data.
- Konsulter importstatus: Sjekk importstatusen for bygninger i din kommune for å se hvor komplett dataene er.

PRØVDE

```terminal
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
```

## Kommentar:
Osmium tags-filter-kommando fungerer som forventet, men her er noen viktige punkter for å sikre at du får så komplette data som mulig:

### Dette gjør kommandoen din riktig
Den filtrerer ut alle noder, veier og relasjoner (nwr) som har noen av de oppgitte taggene.
Du fanger opp adresser (addr:*), bygninger (building, building:levels, roof:levels), og noen detaljer som entrance og level.

### Men her er begrensningene
Adresser i Norge er ofte separate noder, og ikke nødvendigvis koblet til bygningene.

Så filtrering på addr:* vil hente dem, men de trenger ikke være på bygningene.

Ikke alle bygninger har addr:*-tagger.

Mange bygninger har bare building=* og kanskje building:levels.

Ikke alle addr:*-tagger er inkludert

Du mangler f.eks. addr:place, som ofte brukes i stedet for addr:street i små tettsteder.

Du fanger ikke opp highway=address (kan være relevant i noen land, ikke Norge)

## NY
```bash
osmium tags-filter data/norway-latest.osm.pbf \
  nwr/addr:country \
  nwr/addr:county \
  nwr/addr:municipality \
  nwr/addr:city \
  nwr/addr:postcode \
  nwr/addr:street \
  nwr/addr:place \
  nwr/addr:housenumber \
  nwr/addr:unit \
  nwr/addr:block \
  nwr/addr:floor \
  nwr/building \
  nwr/building:levels \
  nwr/roof:levels \
  nwr/entrance \
  nwr/level \
  -o data/filtered.osm.pbf \
  --overwrite
```

Dette vil sikre at du fanger opp flere varianter av adressemerking.


---------------20 august
Klart og kort:
Hva du faktisk trenger fra OSM for en postbar norsk adresse
- Må ha:
    - addr:housenumber
    - addr:postcode (4 siffer)
    - addr:city (poststed)
    - ETT av: addr:street eller addr:place

- Land: sett “NO” som default (for Norge‑ekstrakt).
- Postboks: finnes normalt ikke i OSM.
- Fylke/kommune: står sjelden som addr:*. Legg på senere via spatial join (point‑in‑polygon) mot admin‑grenser.

To enkle steg (samme datasett)
- Steg 1: Filtrer Norge‑PBF og eksporter til JSONL (du har allerede addresses.jsonl).
    - Tips: Krev minst addr:housenumber i filteret for mindre støy.

- Steg 2: Konverter JSONL til CSV og skriv KUN komplette adresser etter norske regler.
    - Land settes til “NO” hvis mangler.
    - Behold bare rader med: (street ELLER place) + housenumber + city + postcode (4 siffer).
    - Fylke/kommune lar du stå tomt nå; fylles inn i et senere steg med spatial join.

Under er en liten, trygg endring som gjør at konverteringen bare skriver komplette adresser. Den bruker samme kolonner som før, men hopper over ufullstendige rader.


```python
#!/usr/bin/env python3
import os
import json
import csv
import argparse
import re
from collections import Counter

POSTCODE_RE = re.compile(r"^\d{4}$")

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def first_point(coords):
    if not coords:
        return None, None
    if isinstance(coords[0], (float, int)):
        return coords[1], coords[0]
    return first_point(coords[0])

def is_complete_no(country, city, postcode, street, place, housenumber):
    if not country:
        country = "NO"
    return (
        country == "NO" and
        housenumber and
        city and
        postcode and POSTCODE_RE.match(postcode) and
        ((street and street.strip()) or (place and place.strip()))
    )

def main():
    p = argparse.ArgumentParser(description="Dump raw GeoJSON-Sequence to CSV (only complete NO addresses)")
    p.add_argument("input", nargs="?", default="data/addresses.jsonl")
    p.add_argument("output", nargs="?", default="data/addresses.csv")
    args = p.parse_args()

    output_dir = "data/out/"
    ensure_dir(output_dir)

    header = [
        "delivery_point_id",
        "country_code", "county", "municipality", "city", "zip_code",
        "street_name", "street_number", "place", "suburb", "hamlet", "village",
        "unit", "block", "floor",
        "lat", "lon",
        "building", "building_levels", "roof_levels", "level", "entrance", "elevator", "building_use"
    ]

    stats = Counter()
    total_rows = 0
    written_rows = 0

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
                continue

            props = feat.get("properties", {})
            total_rows += 1
            osm_id = feat.get("id", "")

            def get_val(key):
                val = props.get(key, "").strip()
                if val:
                    stats[key] += 1
                return val

            # Address parts
            country = get_val("addr:country") or "NO"  # default NO
            county = get_val("addr:county")
            muni = get_val("addr:municipality")
            city = get_val("addr:city")
            hamlet = get_val("addr:hamlet")
            village = get_val("addr:village")
            suburb = get_val("addr:suburb")
            place = get_val("addr:place")
            zipcode = get_val("addr:postcode")
            street = get_val("addr:street")
            number = get_val("addr:housenumber")
            unit = get_val("addr:unit")
            block = get_val("addr:block")
            floor = get_val("addr:floor")

            lat, lon = first_point(feat.get("geometry", {}).get("coordinates", []))
            if lat is not None and lon is not None:
                stats["coordinates"] += 1

            # Building (optional extras)
            building = get_val("building")
            building_levels = get_val("building:levels")
            roof_levels = get_val("roof:levels")
            level = get_val("level")
            entrance = get_val("entrance")
            building_use = get_val("building:use")
            elevator = get_val("elevator")
            if not elevator and props.get("highway", "") == "elevator":
                elevator = "yes"
                stats["elevator"] += 1

            # Keep ONLY complete Norwegian postal addresses
            if not is_complete_no(country, city, zipcode, street, place, number):
                continue

            row = [
                osm_id,
                country, county, muni, city, zipcode,
                street, number, place, suburb, hamlet, village,
                unit, block, floor,
                lat, lon,
                building, building_levels, roof_levels, level, entrance, elevator, building_use
            ]
            writer.writerow(row)
            written_rows += 1

    print("✅ Export completed (only complete NO addresses).")
    print(f"Total features scanned: {total_rows}")
    print(f"Written rows: {written_rows}")
    print("===== FIELD STATS (presence in written rows) =====")
    for field in sorted(stats.keys()):
        print(f"{field:20}: {stats[field]}")

if __name__ == "__main__":
    main()
```

Veien videre
- Hvis du vil ha fylke/kommune med: ta CSV/JSONL ut fra dette skriptet, og gjør en spatial join mot kommune- og fylkespolygoner. Da fylles “municipality” og “county”.
- For brev fra utlandet (eksempel): “Øvre Movei 23, 1450 Nesoddtangen, Norway” – dette fanges av reglene over.
