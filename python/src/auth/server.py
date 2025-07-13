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

server = Flask(__name__)
mysql = MySQL(server)

mysql_envs = ["MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DB", "MYSQL_PORT"]

for mysql_env in mysql_envs:
    server.config[mysql_env] = os.environ.get(mysql_env)

rtn_messages = {
    "missing_credentials": "missing credentials",
    "invalid_credentials": "invalid credentials",
    "token_invalid": "not authorized, token invalid",
}


@server.route("/login", methods=["POST"])
def login():
    # Getting info from Basic Authentication Header and check if the request is valid
    auth = request.authorization
    if not auth:
        return rtn_messages["rtn_messages"], 401

    # retrieve username and password
    user = get_username_by_email(auth.username)

    if not user:
        return rtn_messages["invalid_credentials"], 401

    email = user["email"]
    password = user["password"]

    if auth.username != email or auth.password != password:
        return rtn_messages["invalid_credentials"], 401

    return create_jwt(auth.username, os.environ.get("JWT_SECRET"), True)


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


def get_username_by_email(email):
    """
     Fetch the database to retrieve the user using his email.

     Args:
        email (string): The user email

    Returns:
        dict: A dictionary with email and password if the user has been found, false otherwise.
    """
    cursor = mysql.connection.cursor()
    result = cursor.execute(
        "SELECT email, password FROM user WHERE email=%s", email
    )

    # the result should be one exactly (email column is unique)
    if result == 1:
        user_row = result.fetchone()

        return {"email": user_row[0], "password": user_row[1]}

    return False


def create_jwt(username, secret, is_admin):
    """
     Create a JSON Web Token with username, the secret env and a flag to tell
     if the user has administrative privileges.

     Args:
        username (string).
        secret (string).
        is_admin (bool)

    Returns:
        string: The JWT token encoded with HS256 algorithm.
    """
    now = datetime.datetime.now(tz=datetime.timezone.utc)

    return jwt.encode(
        {
            "username": username,
            "exp": now + datetime.timedelta(days=1),
            "iat": now,
            "is_admin": is_admin,
        },
        secret,
        algorithm=["HS256"],
    )


# config entry point listening on port 5000
if __name__ == "__main__":
    # this tells the operation system to listen to all public IPs
    server.run(host="0.0.0.0", port=5000)
