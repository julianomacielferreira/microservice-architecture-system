import os, requests


def auth_login(request):
    """
    Authenticate in the login endpoint at auth service
    """
    authorization = request.authorization

    if not authorization:
        return None, ("missing credential", 401)

    basicAuth = (authorization.username, authorization.password)

    AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL")

    response = requests.post(f"http://{AUTH_SERVICE_URL}/login", auth=basicAuth)

    if response.status_code == 200:
        return response.text, None

    return None, (response.text, response.status_code)
