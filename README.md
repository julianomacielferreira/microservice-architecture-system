## Microservice Architecture System

This is a project I've always have the desire to code (but did not have the time to do it before) and wanted to make my own modifications and improvements (i.e, add new features).

The initial code is based on the tutorial from [freecodecamp youtube channel](https://www.youtube.com/@freecodecamp) called [**Microservice Architecture and System Design with Python & Kubernetes – Full Course**](https://www.youtube.com/watch?v=hmkF77F9TLw).

![Microservice Architecture and System Design with Python & Kubernetes – Full Course](./video-thumbnail.jpg)

## Project Files Structure

@TODO

## Create docker image, tagging and upload to a docker hub repository

@TODO

## Create config files for kubernetes to pull the images

@TODO

## Create secret token using python

```python
import secrets

# Generate a 32-byte (64-character hex string)
secret_key = secrets.token_hex(32)
print(f"Hexadecimal secret key: {secret_key}")
```

## Running the application

@TODO

## Good practices in a production environment

- Do not push configmap / secret files (.yaml files) containing env variables to the repository.

## Explanation of the docker-compose.yml file (at the root of the application):

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

## Problems faced at the initial setup:

- Exception: Can not find valid pkg-config name.
- Specify MYSQLCLIENT_CFLAGS and MYSQLCLIENT_LDFLAGS env vars manually

```bash
$ sudo apt-get install pkg-config python3-dev default-libmysqlclient-dev build-essential
```

## References

- [**Kubernetes**](https://kubernetes.io/)
- [**minikube**](https://minikube.sigs.k8s.io/)
- [**k9s**](https://github.com/derailed/k9s)
- [**Python 3**](https://www.python.org/)
- [**Flask (python framework)**](https://flask.palletsprojects.com/)
- [**MDN Web Docs**](https://developer.mozilla.org/)
