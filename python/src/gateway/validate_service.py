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

import os, requests


def validate_jwt(request):
    """
    Foward the token to the validate endpoint at auth service
    """
    if not "Authorization" in request.headers:
        return None, ("missing credentials.", 401)

    token = request.headers["Authorization"]

    if not token:
        return None, ("missing credentials.", 401)

    AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL")

    response = requests.post(
        f"http://{AUTH_SERVICE_URL}/validate", headers={"Authorization": token}
    )

    # return the decoded token (the claims)
    if response.status_code == 200:
        return response.text, None

    return None, (response.text, response.status_code)
