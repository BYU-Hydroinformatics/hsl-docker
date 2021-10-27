#!/bin/bash

# echo 'Running the initial LAMP setup . . .'
# /bin/bash run.sh
# echo 'Finished . . .'
echo 'Setting up mysql . . .'
/bin/bash db_config.sh
echo 'Finished . . .'
echo 'Installing HydroServerLite . . .'
/bin/bash hs_config.sh
echo 'Finished . . .'
