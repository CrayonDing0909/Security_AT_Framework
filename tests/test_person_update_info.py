import json
import pytest
from utils.data_loader import load_json_data


@pytest.mark.parametrize(
    "person_data", load_json_data("data/testData/peson_update_info.json"))
def test_update_person_info(person_client, person_data):
    data = {
        "personId": person_data["personId"],
        "name": person_data["name"],
        "employeeId": person_data["employeeId"],
        "information": json.dumps(person_data["information"]),
        # json.dumps() 將字典轉為 JSON 字符串
    }
    files = []
    # Add coverImage
    files.append(("coverImage", open(person_data["coverImage"], "rb")))

    response = person_client.update_person_info(
        data=data, files=files)

    assert response.status_code == 200
