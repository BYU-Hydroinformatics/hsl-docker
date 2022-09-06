#!/bin/bash

#note that the mysql does not have a root password with it
# we can improved by providing a root password with an env variable
# we can improved by providing a the database name, database user name and password to be env variables

if ! mysql -u root -e "use ${HS_DB_NAME}"; then
    echo "creating database"
    mysql --user=root --execute="CREATE DATABASE ${HS_DB_NAME};"
    echo "assingning user and pass"
    mysql --user=root --execute="CREATE USER '${HS_DB_USERNAME}'@'localhost' identified by '${HS_DB_USERNAME_PASS}';"
    echo "granting permissions"
    mysql --user=root --execute="grant all on ${HS_DB_NAME}.* to ${HS_DB_USERNAME}@localhost identified by '${HS_DB_USERNAME_PASS}';"
    echo "Changing mysql root password to the one in the hs.env file"
    mysql --user=root --execute="SET PASSWORD FOR 'root'@'localhost' = PASSWORD('${MYSQL_ROOT_PASSWORD}');FLUSH PRIVILEGES;"

fi