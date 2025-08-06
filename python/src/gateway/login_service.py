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
import requests


class Authenticator:
    """
        Class responsible for authenticating HTTP requests with an authentication service.

        Provides methods for authenticating requests and obtaining authentication tokens.
    """

    def __init__(self, auth_service_url):
        self.AUTH_SERVICE_URL = auth_service_url

    def login(self, request):
        """
          Authenticates at the login endpoint in the authentication service.

          Args:
               request (Request): HTTP request containing authentication credentials.

          Returns:
              tuple: A tuple containing the authentication token and an error (if any).
                    - token (str): Authentication token if authentication is successful.
                    - error (tuple): Tuple containing the error message and HTTP status code if authentication fails.

        """
        authorization = request.authorization

        if not authorization:
            return None, ("missing credential", 401)

        basic_auth = (authorization.username, authorization.password)

        response = requests.post(f"http://{self.AUTH_SERVICE_URL}/login", auth=basic_auth)

        if response.status_code == 200:
            return response.text, None

        return None, (response.text, response.status_code)
