import json
import pytest
from utils.data_loader import load_json_data


@pytest.mark.parametrize(
    "person_data", load_json_data("data/testData/person_update.json"))
def test_update_person(person_client, person_data):
    data = {
        "personId": person_data["personId"],
        "name": person_data["name"],
        "employeeId": person_data["employeeId"],
        "information": json.dumps(person_data["information"]),
        "groupId": person_data["groupId"],
        "skipQC": str(person_data["skipQC"])
    }
    # image column(List of tuples)
    files = []

    files.append(("coverImage", open(person_data["coverImage"], "rb")))
    # handle 1-5 snapshot
    for img_path in person_data["snapshot"]:
        files.append(("Snapshot", open(img_path, "rb")))

    response = person_client.update_person(
        data=data,
        files=files
    )
    """
    目前response只會返回 personId
    1. 請RD新增response其他內容
    2. 如果RD不會新增其他內容,可能改成我們去DB 查詢 personId 的其他資料
    """
    assert response["personId"] == person_data["personId"]
    # 目前 response 只會返回 personId
    # assert response["name"] == person_data["name"]
    # assert response["employeeId"] == person_data["employeeId"]
    # assert response["information"]["email"] ==
    # person_data["information"]["email"]
    # assert response["information"]["company"] ==
    # person_data["information"]["company"]
    # assert response["information"]["title"] ==
    # person_data["information"]["title"]
    # assert response["information"]["note"] ==
    # person_data["information"]["note"]
    # assert response["groupId"] == person_data["groupId"]
    # assert response["skipQC"] == person_data["skipQC"]
