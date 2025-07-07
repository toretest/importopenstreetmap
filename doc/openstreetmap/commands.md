
-------
osmium export data/filtered.osm.pbf \
  --output-format=text |
grep -Ei '(entrance|level|building)'

--------
grep -E "entrance|level|building" data/addresses.csv

--------
grep -i "Øvre Movei" data/addresses.csv

--------
awk -F',' 'NR==1 || tolower($7) ~ /øvre movei/' data/addresses.csv

--------
awk -F',' 'NR==1 || $13 != ""' data/addresses.csv

Explanation:
• -F',' sets the field delimiter to comma.
• NR==1 || $13 != "" prints the header row (NR==1) or any row where the 13th column is not empty.
