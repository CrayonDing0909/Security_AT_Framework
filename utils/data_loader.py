import json
from pathlib import Path


def load_test_data(test_type, endpoint):
    """
    加載測試數據
    :param test_type: 'positive' 或 'negative'
    :param endpoint: 具體的端點名稱，如 'person_import', 'face_add' 等
    """
    file_path = Path(f"data/testData/{test_type}/{endpoint}.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_positive_test_data(endpoint):
    """加載正常測試數據的快捷方法"""
    return load_test_data("positive", endpoint)


def load_negative_test_data(endpoint):
    """加載錯誤測試數據的快捷方法"""
    return load_test_data("negative", endpoint)
