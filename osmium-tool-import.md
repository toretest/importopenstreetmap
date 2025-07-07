# doc


osmium fileinfo data/filtered.osm.pbf

Name: data/filtered.osm.pbf
Format: PBF
Compression: none
Size: 29110578
Header:
Bounding boxes:
(-11.36801,57.55323,35.52711,81.05195)
With history: no
Options:
generator=osmium/1.18.0
osmosis_replication_base_url=https://download.geofabrik.de/europe/norway-updates
osmosis_replication_sequence_number=4474
osmosis_replication_timestamp=2025-07-05T20:21:19Z
pbf_dense_nodes=true
pbf_optional_feature_0=Sort.Type_then_ID
sorting=Type_then_ID
timestamp=2025-07-05T20:21:19Z
(.venv) toregardandersen@tores-Mac-Studio importopenstreetmap 



osmium fileinfo -e data/filtered.osm.pbf


grep -i 'Øvre Movei' data/addresses.csv | grep ',23,'

zise:
du -h data/addresses.csv
ls -lh data/addresses.csv

awk -F, '
$3=="Øvre Movei" && $4=="23" {
print "uid: "        $1
print "postcode: "   $2
print "street: "     $3
print "housenumber: "$4
print "lat: "        $5
print "lon: "        $6
exit
}
' data/addresses.csv

