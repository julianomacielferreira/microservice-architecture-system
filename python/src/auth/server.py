"""
The MIT License

Copyright 2025 Juliano Maciel.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

from auth_service import AuthService

server = Flask(__name__)
mysql = MySQL(server)

mysql_envs = ["MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DB"]

for mysql_env in mysql_envs:
    server.config[mysql_env] = os.environ.get(mysql_env)

# separate MYSQL_POST because it must be an integer not string
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))

rtn_messages = {
    "missing_credentials": "missing credentials",
    "invalid_credentials": "invalid credentials",
    "token_invalid": "not authorized, token invalid",
}

auth_service = AuthService(mysql, os.environ.get("JWT_SECRET"))


@server.route("/login", methods=["POST"])
def login():
    # Getting info from Basic Authentication Header and check if the request is valid
    auth = request.authorization
    if not auth:
        return rtn_messages["rtn_messages"], 401

    # retrieve username and password
    user = auth_service.get_username_by_email(auth.username)

    if not user:
        return rtn_messages["invalid_credentials"], 401

    email = user["email"]
    password = user["password"]

    if auth.username != email or auth.password != password:
        return rtn_messages["invalid_credentials"], 401

    return auth_service.create_jwt(auth.username, os.environ.get("JWT_SECRET"), True)


@server.route("/validate", methods=["POST"])
def validate():
    jwt_token = request.headers["Authorization"]

    if not jwt_token or not jwt_token.startswith("Bearer"):
        return rtn_messages["rtn_messages"], 401

    jwt_token = jwt_token.split(" ")[1]

    try:

        decoded_jwt_token = jwt.decode(
            jwt_token, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )

    except:
        return rtn_messages["token_invalid"], 403

    return decoded_jwt_token, 200


# config entry point listening on port 5000
if __name__ == "__main__":
    # this tells the operation system to listen to all public IPs
    server.run(host="0.0.0.0", port=5000)
