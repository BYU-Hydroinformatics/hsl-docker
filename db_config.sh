#!/bin/bash

#note that the mysql does not have a root password with it
# we can improved by providing a root password with an env variable
# we can improved by providing a the database name, database user name and password to be env variables

mysql --user=root --execute="CREATE DATABASE hydrodb;"
mysql --user=root --execute="CREATE USER 'hydrouser'@'localhost' identified by 'mypass';"
mysql --user=root --execute="grant all on hydrodb.* to hydrouser@localhost identified by 'mypass';"
