# conftest.py
import pytest
from utils.config_loader import get_config
from api_client.auth_client import AuthClient
from api_client.person_client import PersonClient
from api_client.face_client import FaceClient
import os
from _pytest.nodes import Item
from test_order import ordered_modules
from utils.data_loader import load_positive_test_data, load_negative_test_data


def pytest_collection_modifyitems(items: list[Item]):
    def sort_key(item: Item):
        # 取出測試檔案名稱（不含副檔名）
        module_name = os.path.splitext(os.path.basename(item.fspath))[0]
        # item.fspath 會取得測試函式所屬的檔案路徑
        try:
            return ordered_modules.index(module_name)
        except ValueError:
            # 若不在排序清單中，排到最後
            return len(ordered_modules)

    items.sort(key=sort_key)


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store",
        default="dev",
        help="環境名稱：dev/staging/production")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
# Use session scope to load config once per test session
def config(env):
    return get_config(env)

# -----------------------
# 以上為測試環境設定
# -----------------------


@pytest.fixture(scope="session")
# -----------------------
# 認證用戶端（共用登入）
# -----------------------
def auth_client(config):
    return AuthClient(
        base_url=config["base_url"],  # get base_url from config
        username=config["account"],  # get account from config
        password=config["password"]  # get password from config
    )


@pytest.fixture(scope="module")
# -----------------------
# 人員管理用戶端（每個模組可共用）
# -----------------------
def person_client(auth_client):
    return PersonClient(
        base_url=auth_client.base_url,
        token=auth_client.token
    )


@pytest.fixture(scope="module")
def face_client(auth_client):
    return FaceClient(
        base_url=auth_client.base_url,
        token=auth_client.token
    )


@pytest.fixture(scope="function")
def positive_test_data(request):
    """
    Fixture for loading positive test data
    Usage: def test_something(positive_test_data):
        data = positive_test_data('endpoint_name')
    """
    def _load_data(endpoint):
        return load_positive_test_data(endpoint)
    return _load_data


@pytest.fixture(scope="function")
def negative_test_data(request):
    """
    Fixture for loading negative test data
    Usage: def test_something(negative_test_data):
        data = negative_test_data('endpoint_name')
    """
    def _load_data(endpoint):
        return load_negative_test_data(endpoint)
    return _load_data
