#!bin/bash


echo "Deleting duplicated time series"

SQL_Query='delete from seriescatalog where SeriesID not in (select min(SeriesID) from (select * from seriescatalog) as sc  group by SiteID, VariableID);'
# mysql -d hydrodb" -e "DELETE FROM seriescatalog WHERE SeriesID NOT IN SELECT min(SeriesID) FROM SELECT * FROM seriescatalog as sc GROUP BY SiteID, VariableID;"

# dbname='hydrodb'
dbname=$HS_DB_NAME
mysql -D $dbname <<EOF
$SQL_Query
EOF

echo "Done"
