import pytest
from utils.data_loader import load_json_data


@pytest.mark.parametrize(
    "person_data", load_json_data("data/testData/person_delete.json"))
def test_delete_person(person_client, person_data):
    response = person_client.delete_person(data=person_data)
    assert response.status_code == 200
