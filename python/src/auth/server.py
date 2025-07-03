import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

mysql_envs = ["MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DB", "MYSQL_PORT"]

for mysql_env in mysql_envs:
    server.config[mysql_env] = os.environ.get(mysql_env)


@server.route("/login", methods=["POST"])
def login():
    # Getting info from Basic Authentication Header
    auth = request.authorization()
    if not auth:  # request invalid
        return "missing credentials", 401

    # check db for username and password
