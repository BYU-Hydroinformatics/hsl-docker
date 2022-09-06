## Description

- This is the docker image for the **[HydroServerLite](https://github.com/CUAHSI/HydroServerLite)** project, but it does not uses such repository, but the one called [hsl-interactive](https://github.com/BYU-Hydroinformatics/hsl-interactive)

## Installation

- Run docker-compose commands:
  ```bash
  	  docker-compose build --no-cache
  	  docker-compose up
  ```
- Exporting data from a sql file

  - Run the following command to create the tables of the selected db
    - `cat <BACKUP_FILE.sql> | docker exec -i <CONTAINER_NAME> /usr/bin/mysql -u <USER> -p<PASSWORD> <DATABASENAME>`
  - **Note** Do not run the installation at

    - _http://localhost/hydroserverlite/index.php/default/home/installation_

    before doing this if you plan to import data from another hydroserver

  - Fill the installation form at:
    - `<DOMAIN>/hydroserverlite/index.php/default/home/installation`
    - Example:
      - `http://localhost/hydroserverlite/index.php/default/home/installation`

## Notes

### Environment variables

- The **HS_DB_NAME** that is in the _.env_ file has the same name as the name of the hydroserver installation

### Exporting data

- Exporting data should be done with the following command:

  `mysqldump -u<DB_USER> -p<DB_PASS> <DB_NAME> > <PATH_TO_SQL_FILE>`

- Exporting from a docker container

  `docker exec <container_name> sh -c 'exec mysqldump --all-databases -u<user> -p<password> <database>' > /some/path/on/your/host/all-databases.sql`

### Database Configuration

- Changing **root password** is done with the following commands in the **db_config.sh** (because it is a mysql version < 8)

  ```mysql
  SET PASSWORD FOR 'root'@'localhost' = PASSWORD('mypass');
  FLUSH PRIVILEGES;
  ```

- The **db_config.sh** checks with an if statement that the env variable **HS_DB_NAME** exits, otherwise it will not do anything

- env variables are referenced with _${env_variable}_
  - `mysql --user=root --execute="CREATE DATABASE ${HS_DB_NAME};"`

### Hydroserver Configuration

- Clone of the repositorio called [hsl_interactive](https://github.com/BYU-Hydroinformatics/hsl-interactive.git)

- Creation of _uploads_ folder

### Changing of permissions

```bash
cd /var/www/html/hydroserverlite
chmod -R 777 application/config/installations
chmod -R 777 application/language
chmod -R 777 uploads
```

### Customization of the hydroserver instalation with the env variables

```bash
sed -i "s/YOUR_DATABASE_USER_NAME/$HS_DB_USERNAME/" /app/hydroserverlite/application/config/installations/default.php
sed -i "s/YOUR_MYSQL_DATABASE_NAME/$HS_DB_NAME/" /app/hydroserverlite/application/config/installations/default.php
sed -i "s/YOUR_MYSQL_DATABASE_PASSWORD/$HS_DB_USERNAME_PASS/" /app/hydroserverlite/application/config/installations/default.php
```

- **Note** the use of the env variables in the **.env** file

### Supervisord-hs.conf

- Supervisord is design to control programs that run for long times. In this project [[Supervisor]] is used because the [LAMP docker image](https://hub.docker.com/r/mattrayner/lamp) used uses Supervisor to start mysql and the Apache server.

- Supervisor runs the bash script **final_run** which runs all the necessary configuration including (db, hydroserver, etc) The following is the file:
  ```.conf
  [program:hydroserver]
  command=/final_run.sh
  numprocs=1
  autostart=true
  autorestart=false
  stdout_logfile = /mylogs/hs.log
  redirect_stderr = true
  startsecs = 0
  ```
- **startsecs=0** and **autorestart =false** is used because we need the program to not having restart automatically once is exited (which will do because the program is not supposed to run in the background)

### Final_run.sh

- The script starts with sleeping because the hydroserver program that we have defined in the **Supervisord-hs.conf** starts before the other services (mysql and Apache) defined by Supervisor in the [LAMP docker image](https://hub.docker.com/r/mattrayner/lamp) The Hydroserver service needs to wait for the mysql and Apache to start.

```bash
    echo "Sleeping to wait for mysql to start"
    sleep 10
```
