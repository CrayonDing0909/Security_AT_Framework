def test_sign_in_success(auth_client):
    # print(f"Testing sign-in: {auth_client.username}")  # For debugging
    # print(f"Using base URL: {auth_client.base_url}")  # For debugging
    # print(f"Using password: {auth_client.password}")  # For debugging
    # print(f"Token: {auth_client.token}")  # For debugging
    assert auth_client.token is not None
    assert isinstance(auth_client.token, str)


def test_auth_info(auth_client):
    response = auth_client.get_auth_info()
    data = response.json()
    # print(data)  # For debugging
    assert response.status_code == 200
    assert "accountId" in data
    assert data["account"] == auth_client.username
