import requests


class PersonClient:
    """
    A client for managing person-related operations in the API.
    """
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def import_person_with_images(self, data, files):
        url = f"{self.base_url}/api/website/person/import"
        headers = {"Authorization": self.token}

        # ✅ Debug log
        print("📤 POST URL:", url)
        print("📤 Headers:", headers)
        print("📤 Data Payload:")
        for k, v in data.items():
            print(f"    {k}: {v}")
        print("📤 Files:")
        for name, file_obj in files:
            print(f"    {name}: {file_obj.name}")

        response = requests.post(url, headers=headers, data=data, files=files)

        # # ✅ For Debugging
        print("📥 Response Status Code:", response.status_code)
        print("📥 Response Body:", response.text)

        response.raise_for_status()
        return response.json()

    def query_person(self, personId):
        url = f"{self.base_url}/api/website/person/query"
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/x-www-form-urlencoded"
            }
        params = {"personId": personId}
        # 考慮refine成params

        # ✅ Debug log
        print("📤 POST URL:", url)
        print("📤 Headers:", headers)
        print("📤 Query Parameters:", params)

        response = requests.post(url, headers=headers, params=params)

        # ✅ For Debugging
        print("📥 Response Status Code:", response.status_code)
        print("📥 Response Body:", response.text)

        response.raise_for_status()
        return response.json()

    def update_person(self, data, files=None):
        url = f"{self.base_url}/api/website/person/update"
        headers = {
            "Authorization": self.token,
            }

        print("📤 POST URL:", url)
        print("📤 Headers:", headers)
        print("📤 Data Payload:", data)

        response = requests.post(url, headers=headers, data=data, files=files)

        print("📥 Response Status Code:", response.status_code)
        print("📥 Response Body:", response.text)
        print("📥 Response:", response)

        response.raise_for_status()
        return response.json()

    def update_person_info(self, data, files=None):
        url = f"{self.base_url}/api/website/person/info/update"
        headers = {"Authorization": self.token}

        print("📤 POST URL:", url)
        print("📤 Headers:", headers)
        print("📤 Data Payload:", data)

        response = requests.post(
            url, headers=headers, data=data, files=files
            )

        print("📥 Response Status Code:", response.status_code)
        print("📥 Response Body:", response.text)
        print("📥 Response:", response)

        response.raise_for_status()
        return response  # not json, so return response object directly

    def delete_person(self, data):
        url = f"{self.base_url}/api/website/person/delete"
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/x-www-form-urlencoded"
            }
        params = {"personId": data["personId"]}
        print("📤 POST URL:", url)
        print("📤 Headers:", headers)
        print("📤 params Payload:", params)
        response = requests.post(url, headers=headers, params=params)

        print("📥 Response Status Code:", response.status_code)
        print("📥 Response Body:", response.text)
        print("📥 Response:", response)

        response.raise_for_status()
        return response
