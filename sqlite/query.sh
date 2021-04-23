echo ".tables"                              | sqlite3 -header firetrucks.db
echo "select * from FireTrucks"             | sqlite3 -header firetrucks.db
echo "select * from FirefightingParameters" | sqlite3 -header firetrucks.db
echo "select * from LadderLiftParameters"   | sqlite3 -header firetrucks.db
echo "select * from Generics"               | sqlite3 -header firetrucks.db
