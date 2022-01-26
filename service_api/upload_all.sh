#!/bin/bash
source ~/miniconda3/bin/activate $3

echo "Uploading Sources . . ."

python add_info.py sources http://localhost/hydroserverlite/index.php/default/services/api ../data_test/sources.csv $1 $2

echo "Uploading Variables . . ."

python add_info.py variables http://localhost/hydroserverlite/index.php/default/services/api ../data_test/variables.csv $1 $2

echo "Uploading Sites . . ."

python add_info.py sites http://localhost/hydroserverlite/index.php/default/services/api ../data_test/SitesPruebaReduced.csv $1 $2

echo "Uploading Time Series . . ."

python add_info.py values http://localhost/hydroserverlite/index.php/default/services/api ../data_test/dataValuesReduced.csv $1 $2

echo "Deleting duplicates in series . . ."

docker exec -i hs_d bash < ../delete_duplicates.sh

echo "Done . . . "
