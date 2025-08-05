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

from flask_mysqldb import MySQL
import jwt
import datetime


class AuthService:
    """
        Authentication service responsible for managing user authentication.

        Attributes:
            mysql (MySQL): MySQL instance for database connection.
            secret (str): Secret key for signing JWT tokens.

        Methods:
            get_username_by_email(email): Retrieves user information based on email.
            create_jwt(username, is_admin): Creates a JWT token for the user.

    """

    def __init__(self, mysql, secret):
        self.mysql = mysql
        self.secret = secret

    def get_username_by_email(self, email):
        """
         Fetch the database to retrieve the user using his email.

         Args:
            email (string): The user email

        Returns:
            dict: A dictionary with email and password if the user has been found, false otherwise.
        """
        query = f"SELECT email, password FROM user WHERE email='{email}'"
        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        # the result should be one exactly (email column is unique)
        if result == 1:
            return {"email": result[0], "password": result[1]}

        return False

    def create_jwt(self, username, is_admin):
        """
         Create a JSON Web Token with username, the secret env and a flag to tell
         if the user has administrative privileges.

         Args:
            username (string).
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
            self.secret,
            algorithm=["HS256"],
        )
