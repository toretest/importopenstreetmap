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