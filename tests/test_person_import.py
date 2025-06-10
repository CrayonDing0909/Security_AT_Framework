import json
import pytest
from utils.data_loader import load_positive_test_data


@pytest.mark.parametrize(
    "person_data", 
    load_positive_test_data("person_import")
)
def test_import_person_success(person_client, person_data):
    # 🔧 將資料轉為 form-data 格式
    data = {
        "name": person_data["name"],
        "employeeId": person_data["employeeId"],
        "information": json.dumps(person_data["information"]),
        "groupId": person_data["groupId"],
        "skipQC": str(person_data["skipQC"])
    }

    # ✅ image column(List of tuples)
    files = []

    # add coverImage
    files.append(("coverImage", open(person_data["coverImage"], "rb")))

    # handle 1-5 snapshot
    for img_path in person_data["snapshot"]:
        files.append(("snapshot", open(img_path, "rb")))

    response = person_client.import_person_with_images(data, files)
    assert isinstance(response["personId"], int)
    assert response["operation"] == "CREATE"
    """
    Response Body: {"personId":x,"operation":"CREATE"}
    """
