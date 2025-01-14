from google.cloud import storage
import os
import json
import re
import csv

# 初始化 GCS 客戶端
client = storage.Client()

# 設定參數
BUCKET_NAME = "pyspark-lda-test"
PREFIX = "爬蟲資料/爬蟲資料/"
CLEANED_DATA_DIR = "cleaned-data/"  # 清洗後數據保存的 GCS 路徑
PROCESSED_FILES_LOG = "processed_files.log"  # 紀錄已處理檔案的檔案名稱

# 清除 HTML 標籤的函數
def clean_html(raw_html):
    """
    移除 HTML 標籤和特殊字符，保留純文字
    """
    cleanr = re.compile('<.*?>')  # 匹配 HTML 標籤
    text = re.sub(cleanr, '', str(raw_html)).strip()  # 確保為字符串後移除 HTML 標籤
    text = re.sub(r'\\u[0-9a-fA-F]{4}', '', text)  # 去掉 \uXXXX 編碼
    text = re.sub(r'\s+', ' ', text)  # 合併多餘空格
    return text

# 讀取已處理的檔案紀錄
def load_processed_files():
    """
    載入已處理檔案的名稱
    """
    if os.path.exists(PROCESSED_FILES_LOG):
        with open(PROCESSED_FILES_LOG, 'r', encoding='utf-8') as log_file:
            return set(log_file.read().splitlines())
    return set()

# 紀錄已處理的檔案
def save_processed_file(filename):
    """
    儲存已處理檔案的名稱到紀錄檔
    """
    with open(PROCESSED_FILES_LOG, 'a', encoding='utf-8') as log_file:
        log_file.write(f"{filename}\n")

# 主邏輯
def extract_and_clean_data():
    """
    從 GCS 下載 JSON 文件，提取並清洗所需欄位內容，並將清洗後的數據上傳至 GCS
    """
    bucket = client.bucket(BUCKET_NAME)
    blobs = list(client.list_blobs(BUCKET_NAME, prefix=PREFIX))

    # 讀取已處理的檔案
    processed_files = load_processed_files()

    for blob in blobs:
        if blob.name.endswith('.json') and blob.name not in processed_files:
            print(f"Processing {blob.name}...")
            local_path = f"/tmp/{os.path.basename(blob.name)}"

            # 下載文件
            blob.download_to_filename(local_path)

            # 清洗後的數據存放在列表中
            cleaned_data = []

            # 讀取並處理 JSON 文件
            with open(local_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    # 確保 data 是列表
                    if isinstance(data, list):
                        for item in data:
                            # 確保 item 是字典
                            if isinstance(item, dict):
                                node = item.get("node", {})
                                body = clean_html(node.get("body", ""))
                                created_time = node.get("created_time", "")
                                nid = node.get("nid", "")
                                title = clean_html(node.get("article_category", ""))

                                # 添加清洗後的數據
                                cleaned_data.append({
                                    "created_time": created_time,
                                    "nid": nid,
                                    "title": title,
                                    "body": body
                                })
                            else:
                                print(f"Skipping invalid item in {blob.name}: {item}")
                    else:
                        print(f"Skipping invalid JSON format in {blob.name}")
                except json.JSONDecodeError:
                    print(f"Invalid JSON file: {blob.name}")

            # 保存清洗後的數據到臨時 CSV 文件
            output_file = f"/tmp/cleaned_{os.path.basename(blob.name)}.csv"
            with open(output_file, 'w', encoding='utf-8-sig', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=["created_time", "nid", "title", "body"])
                writer.writeheader()
                writer.writerows(cleaned_data)

            print(f"Cleaned data saved to {output_file}")

            # 將清洗後的 CSV 文件上傳至 GCS
            cleaned_blob_name = f"{CLEANED_DATA_DIR}cleaned_{os.path.basename(blob.name)}.csv"
            cleaned_blob = bucket.blob(cleaned_blob_name)
            cleaned_blob.upload_from_filename(output_file)
            print(f"Uploaded cleaned data to GCS: {cleaned_blob_name}")

            # 移除本地文件
            os.remove(local_path)
            os.remove(output_file)

            # 紀錄處理過的檔案
            save_processed_file(blob.name)

if __name__ == "__main__":
    extract_and_clean_data()
