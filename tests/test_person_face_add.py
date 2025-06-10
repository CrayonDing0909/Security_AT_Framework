import pytest
from utils.data_loader import load_positive_test_data


@pytest.mark.parametrize(
    "person_data",
    load_positive_test_data("face_add")
)
def test_add_person_face(face_client, person_data):
    data = {
        "personId": person_data["personId"],
    }
    files = []
    files.append(("snapshot", open(person_data["snapshot"], "rb")))
    response = face_client.add_person_face(data, files)
    assert isinstance(response["faceId"], list)
