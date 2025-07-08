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
