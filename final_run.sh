#!/bin/bash
echo "Sleeping to wait for mysql to start"
sleep 10

echo 'Setting up mysql database: Basically checking if the db and db user were setup. . .'
/bin/bash db_config.sh
echo 'Finished . . .'
echo 'Installing HydroServerLite basically copying files etc. . .'
/bin/bash hs_config.sh
echo 'Finished . . .'
