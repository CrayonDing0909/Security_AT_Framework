import requests


class AuthClient:
    """
    A client for handling authentication with the API.
    responsible for signing in and retrieving authentication information.
    """
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.token = self._sign_in()

    def _sign_in(self):
        url = f"{self.base_url}/api/website/account/signIn"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "account": self.username,
            "password": self.password,
            "expiryDay": -1
        }
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("token")

    def get_auth_info(self):
        url = f"{self.base_url}/api/website/account/info"
        headers = {"Authorization": self.token}
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response  # Return the response object for further processing
