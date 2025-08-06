"""
The MIT License

Copyright 2025 Juliano Maciel Maciel.

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
import requests


class JWTValidator:
    """
        Class responsible for validating JWT tokens with an authentication service.

        Provides methods for validating tokens and obtaining decoded claims.
    """

    def __init__(self, auth_service_url):
        """
        Initializes the class with the authentication service URL.

        Args:
            auth_service_url (str, optional): Authentication service URL. Defaults to None.
        """
        self.AUTH_SERVICE_URL = auth_service_url

    def validate(self, request):
        """
        Validates a JWT token by forwarding it to the validation endpoint in the authentication service.

        Args:
            request (Request): HTTP request containing the JWT token.

        Returns:
            tuple: A tuple containing the decoded claims and an error (if any).
                - claims (str): Decoded claims if validation is successful.
                - error (tuple): Tuple containing the error message and HTTP status code if validation fails.
        """
        if not "Authorization" in request.headers:
            return None, ("missing credentials.", 401)

        token = request.headers["Authorization"]

        if not token:
            return None, ("missing credentials.", 401)

        response = requests.post(
            f"http://{self.AUTH_SERVICE_URL}/validate", headers={"Authorization": token}
        )

        if response.status_code == 200:
            # return the decoded token (the claims)
            return response.text, None

        return None, (response.text, response.status_code)
