import requests


class FaceClient:
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def add_person_face(self, data, files):
        url = f"{self.base_url}/api/website/person/face/create"
        headers = {"Authorization": self.token}
        response = requests.post(url, headers=headers, data=data, files=files)
        # ✅ For Debugging
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)

        response.raise_for_status()
        return response.json()

    def search_face(self, data, files):
        url = f"{self.base_url}/api/website/search/face"
        headers = {"Authorization": self.token}
        response = requests.post(url, headers=headers, data=data, files=files)
        # ✅ For Debugging
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)
        response.raise_for_status()
        return response.json()
