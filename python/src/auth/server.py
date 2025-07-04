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
    user = get_username_by_email(auth.username)

    if not user:
        return "invalid credentials", 401

    email = user["email"]
    password = user["password"]

    if auth.username != email or auth.password != password:
        return "invalid credentials", 401

    return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)


def get_username_by_email(email):
    cursor = mysql.connection.cursor()
    result = cursor.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username)
    )

    # the result should be one exactly (email column is unique)
    if result == 1:
        user_row = result.fetchone()

        return {"email": user_row[0], "password": user_row[1]}

    return False


def createJWT(username, secret, is_admin):

    THIS_TIME = datetime.datetime.now(tz=datetime.timezone.utc)

    return jwt.encode(
        {
            "username": username,
            "exp": THIS_TIME + datetime.timedelta(days=1),
            "iat": THIS_TIME,
            "is_admin": is_admin,
        },
        secret,
        algorithm=["HS256"],
    )
