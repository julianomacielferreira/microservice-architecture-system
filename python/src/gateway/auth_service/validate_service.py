import os, requests


def validate_jwt(request):
    if not "Authorization" in request.headers:
        return None, ("missing credentials.", 401)

    token = request.headers["Authorization"]

    if not token:
        return None, ("missing credentials.", 401)

    response = requests.post(
        f"http://{os.environ.get("AUTH_SERVICE_URL")}/validate",
        headers={"Authorization" : token}
    )

    if response.status_code == 200:
        return response.text, None
    
    return None, (response.text, response.status_code)