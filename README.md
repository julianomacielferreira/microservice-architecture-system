## Microservice Architecture System

@TODO

## Explanation of the docker-compose.yml file:

```yml
version: '3.8': Specifies the Docker Compose file format version.

services: Defines the services (containers) that make up your application.
    mysql_db: The name of your MySQL service.
    image: mysql:8.0: Uses the official MySQL 8.0 Docker image. You can specify a more precise version if needed (e.g., mysql:8.0.30).
    container_name: mysql_8_database: Assigns a custom name to your container for easier identification.
    restart: always: Ensures the container restarts automatically if it stops or the Docker daemon restarts.
    environment: Sets environment variables within the container.
        MYSQL_ROOT_PASSWORD: Sets the password for the root user.
        MYSQL_DATABASE: Creates a new database with the specified name when the container starts.
        MYSQL_USER: Creates a new user with the specified username (do not use "root").
        MYSQL_PASSWORD: Sets the password for the new user.
    ports: - "3306:3306": Maps port 3306 on your host machine to port 3306 inside the container, allowing external connections to MySQL.
    volumes: 
        - mysql_data:/var/lib/mysql: Mounts a named volume (mysql_data) to the /var/lib/mysql directory inside the container. This persists your database data even if the container is removed.

volumes: Defines the named volumes used in your services.
    mysql_data: The named volume for your MySQL data.
        driver: local: Specifies that the volume should be stored locally on your host machine.
```

## Solve the problem:

- Exception: Can not find valid pkg-config name. 
- Specify MYSQLCLIENT_CFLAGS and MYSQLCLIENT_LDFLAGS env vars manually

```bash
$ sudo apt-get install pkg-config python3-dev default-libmysqlclient-dev build-essential
```
