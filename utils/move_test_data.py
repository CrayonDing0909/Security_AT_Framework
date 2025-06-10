import shutil
from pathlib import Path

def move_test_data():
    # 創建目標目錄
    positive_dir = Path("data/testData/positive")
    positive_dir.mkdir(parents=True, exist_ok=True)
    
    # 要移動的文件映射
    file_mapping = {
        "person_import.json": "person_import.json",
        "person_query.json": "person_query.json",
        "person_update.json": "person_update.json",
        "peson_update_info.json": "person_update_info.json",  # 修正拼寫錯誤
        "person_delete.json": "person_delete.json",
        "person_face_add.json": "face_add.json"
    }
    
    # 移動文件
    for src_name, dst_name in file_mapping.items():
        src_path = Path("data/testData") / src_name
        dst_path = positive_dir / dst_name
        if src_path.exists():
            shutil.move(str(src_path), str(dst_path))
            print(f"Moved {src_name} to {dst_name}")

if __name__ == "__main__":
    move_test_data() 