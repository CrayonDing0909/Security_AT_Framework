import pytest
from utils.data_loader import load_positive_test_data


@pytest.mark.parametrize(
    "person_data", 
    load_positive_test_data("person_query")
)
def test_query_person_success(person_client, person_data):
    response = person_client.query_person(person_data["personId"])
    assert response["personId"] == person_data["personId"]
    """
    Response Body: {
    "personId":1,
    "name":"Dylan Ding",
    "employeeId":"123456",
    "information":{"email":"test email",
    "company":"test company",
    "title":"test title",
    "note":"test note"},
    "faces":[{"faceId":1,"snapshotUrl":"/image/s/1?ts=1748485389210","isSelected":true}],
    "group":[{"groupId":1,"name":"VIP","type":"VIP",
    "tags":[],
    "isLifespanEnabled":false,
    "displayPrecisionFilter":false}],
    "firstVisited":null,
    "lastVisited":null,
    "visitedCount":0,
    "visitedCountInHalfYear":0,
    "coverImageUrl":"/image/p/1",
    "isUploadCoverImage":true,
    "isLifespanEnabled":false
    }
    """
