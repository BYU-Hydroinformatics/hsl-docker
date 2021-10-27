#!/bin/bash

# get the latest HydroServer Lite Files and then move them into the html folder
git clone https://github.com/HydroServerLite/master.git /hydroserverlite

mv hydroserverlite var/www/html/hydroserverlite

# setup the HydroServer file permissions
chmod -R 777 var/www/html/hydroserverlite/application/config/installations
chmod -R 777 var/www/html/hydroserverlite/application/language
chmod -R 777 var/www/html/hydroserverlite/uploads

# create the default installation file: replace the mysql username, mysql db name, and mysql password.
# and save it as application/config/installations/default.php.

sed -i 's/YOUR_DATABASE_USER_NAME/hydrouser/' var/www/html/hydroserverlite/application/config/installations/sample_installation_file.txt
sed -i 's/YOUR_MYSQL_DATABASE_NAME/hydrodb/' var/www/html/hydroserverlite/application/config/installations/sample_installation_file.txt
sed -i 's/YOUR_MYSQL_DATABASE_PASSWORD/mypass/' var/www/html/hydroserverlite/application/config/installations/sample_installation_file.txt
mv var/www/html/hydroserverlite/application/config/installations/sample_installation_file.txt var/www/html/hydroserverlite/application/config/installations/default.php
