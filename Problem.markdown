## 5/24目前先將基礎架構構建好,將api_client, tests, utils,建置好
    1. 目前先撰寫authentication, 看能不能完整的架構,先都走得下去, 再慢慢進行擴展, 
    2. utils用了config_loder.py我想要把她分不同的設定檔,像是dev.json, staging.json,讓他不是寫死在code裡,可以集中管理config
    3.整體流程:
        使用者下command
        pytest test/ --env dev
        conftest.py 接收參數 → env="dev"
        get_config(env) → 讀取 config/dev.json

## 5/25 目前Auth的流程順序(怕我忘記)
    1. 使用者輸入 pytest tests/test_auth.py --env dev 指令
    2. pytest 開始去tests/裡找測試項, 掃描到 test_auth.py，找到兩個函式：
     - test_sign_in_success(auth_client)
     - test_auth_info(auth_client)
    3. 發現這兩個函式都需要一個叫 auth_client 的參數
    4. pytest 去找 fixture: auth_client()
    5. 執行 fixture：
      → 建立 AuthClient(base_url, username, password)
      → 呼叫 __init__ → 執行 self._sign_in()
      → 儲存 self.token
    6. fixture 回傳這個 AuthClient 實例給兩個測試函式
    7. 測試函式執行，使用這個物件的 .token, .get_auth_info() 等方法

## Pytest fixture 的 scope 類型總覽（由小到大）
| scope                 | 被呼叫的頻率                               | 使用時機               |
| ----------------      | ---------------------------               | ------------------ |
| `"function"`(預設)    | 每一個測試函式都會**重新執行一次 fixture**   | 測試資料需要「乾淨獨立」時最保險   |
| `"class"`             | 每個測試類別執行一次                        | 同一類別底下的測試都共用一組資料   |
| `"module"`            | 每個 `.py` 測試模組執行一次                 | 適合整個檔案裡都用同一份登入/設定  |
| `"session"`           | 整個 pytest session 只執行一次              | 適合整套測試用同一個登入/初始化流程 |

# Q:fixture 是怎麼做到以上這種共用機制的?

## 如果你這樣改：
@pytest.fixture(scope="session")
def auth_client(config):
    return AuthClient(...)
那麼：
整個 pytest 執行過程只會執行一次 AuthClient(...)
所有測試檔案中的 auth_client 都會使用同一個 token（共用登入）

## fixture怎麼做到這種共用機制的？
這是 pytest 的 fixture caching 系統的設計：
Pytest 背後會這樣管理：
_fixture_cache = {}
def resolve_fixture(name, scope):
    if name in _fixture_cache[scope]:
        return _fixture_cache[scope][name]
    else:
        result = run_fixture(name)
        _fixture_cache[scope][name] = result
        return result
也就是：相同 scope + 相同 fixture 名稱 → pytest 會重用它（不重新建立）

  ### 使用 scope="module" 時會怎樣？
  | 測試檔案         | 執行時會做什麼                      |
  | --------------- | ---------------------------- |
  | test\_face.py   | 執行一次 `auth_client()` → 登入一次  |
  | test\_person.py | 執行一次 `auth_client()` → 再登入一次 |
  | test\_record.py | 執行一次 `auth_client()` → 再登入一次 |

  ### 使用 scope="session" 時會怎樣？
  | 測試檔案            | 執行時會做什麼                     |
  | --------------- | ------------------------------ |
  | test\_face.py   | ✅ 第一次執行 `auth_client()` → 登入一次 |
  | test\_person.py | 🔁 共用上一個 `auth_client` 實例      |
  | test\_record.py | 🔁 共用上一個 `auth_client` 實例      |

  ### 要 debug fixture 被執行幾次
  print(f"[DEBUG] 建立 auth_client for {request.scope}")

## 執行personClient前會先去執行 auth_client fixture

    pytest test_xxx.py
    └──> 發現需要 person_client fixture
         └──> 先執行 auth_client fixture（如果還沒建立）
              └──> 建立 AuthClient → 自動登入取得 token
         └──> 建立 PersonClient(base_url, token)
                 └──> token 是從 auth_client.token 傳入

# Design person_import_client遇到的問題
| 問題描述                        | 錯誤訊息 / 行為                                   | 解法                                             |
| ---------------------------     | ------------------------------------------- | ---------------------------------------------------------|
| **未建立 tag 時送出 `tags` 欄位**   | `400 Bad Request: Tag 'xxx' does not exist`           | ✅ 略過tag的不建立,目前看起來只能在Central上手動建立 |
| **未處理 `information` 欄位格式**  | `400 Bad Request`                                      | ✅ 使用 `json.dumps()` 將 dict 轉成 JSON 字串       |
| **同一人重複 enroll**        | `406 Not Acceptable errorMessage":"Exists similar person.`   | ✅ 測試前清除測資,未來考慮 建立 tag 時自動檢查存在性，避免失敗 |

# 25/6/2目前已將person的endpoint design完,也可以正常執行了,但目前有個問題是,我要排他的執行order, 不能還沒新增就刪除, 所以目前有幾種方式
## 1.直接給編號test_01_import, test_02....以此類推(目前後續可能不好維護,要改名字,後續固定)
## 2.使用 pytest-order 套件, 每個測試加上 @pytest.mark.order(x) 的decorator

## 3.(目前採用)自訂 test collection 排序 + 集中順序管理表
集中管理測試模組順序的設定檔 test_order.py
ordered_modules = [
    "test_person_import",
    "test_person_query",
    "test_person_update",
    "test_person_update_info",
    "test_person_delete"
]
### 🔁 測試模組執行順序控管說明
本專案使用 `conftest.py` 搭配 `test_order.py` 控制 pytest 執行模組的順序。
#### 📌 如何運作？

1. 測試檔案順序統一維護於 `test_order.py` → `ordered_modules` list。
2. Pytest 執行時，會自動依照這個 list 的順序執行各個模組的測試。
3. 未列在清單內的測試模組，將排在最後執行。

#### ✅ 使用方式
pytest tests/ --env dev -s -v
- 使用 `pytest -k test_xxx` 執行單一測試仍有效


