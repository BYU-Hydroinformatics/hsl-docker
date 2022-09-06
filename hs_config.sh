#!/bin/bash

# get the latest HydroServer Lite Files and then move them into the html folder

if [[ -d /app/hydroserverlite ]] ; then
    echo "Hydroserverlite is already installed"


else
    echo "Hydroserverlite not found, starting to install"
    echo "Clonning repo with hydroserverlite"
    git clone --branch docker-version https://github.com/BYU-Hydroinformatics/hsl-interactive.git /app/hydroserverlite

    echo "Clonning repo with hydroserverlite"

    mkdir /app/hydroserverlite/uploads
    # setup the HydroServer file permissions
    echo "setup the HydroServer file permissions"

    cd /var/www/html/hydroserverlite
    chmod -R 777 application/config/installations
    chmod -R 777 application/language
    chmod -R 777 uploads

    # create the default installation file: replace the mysql username, mysql db name, and mysql password.
    # and save it as application/config/installations/default.php.
    echo "create the default installation file: replace the mysql username, mysql db name, and mysql password."

    sed -i "s/YOUR_DATABASE_USER_NAME/$HS_DB_USERNAME/" /app/hydroserverlite/application/config/installations/default.php
    sed -i "s/YOUR_MYSQL_DATABASE_NAME/$HS_DB_NAME/" /app/hydroserverlite/application/config/installations/default.php
    sed -i "s/YOUR_MYSQL_DATABASE_PASSWORD/$HS_DB_USERNAME_PASS/" /app/hydroserverlite/application/config/installations/default.php
fi


