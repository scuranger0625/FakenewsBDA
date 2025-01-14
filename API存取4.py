import requests
import json
import os
import time

# 新 API 端點和 token
base_url = "https://api.tfc-taiwan.org.tw/article-api"
token = "a244fe73-4ecf-4aaf-b322-1e10ff0092f7"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 輸出文件目錄
output_dir = r"C:\Users\Leon\Desktop\事實查核中心資料\爬蟲資料"
progress_file = os.path.join(output_dir, "進度記錄.json")

# 確保輸出目錄存在
os.makedirs(output_dir, exist_ok=True)

# 初始化已完成的頁數
if os.path.exists(progress_file):
    with open(progress_file, "r", encoding="utf-8") as f:
        completed_pages = json.load(f).get("completed_pages", [])
else:
    completed_pages = []

# 開始爬取
current_page = 0  # 從第 0 頁開始

while True:
    if current_page in completed_pages:
        print(f"第 {current_page} 頁已完成，跳過...")
        current_page += 1
        continue

    print(f"正在處理第 {current_page} 頁...")
    params = {
        "token": token,
        "page": current_page
    }

    retries = 5  # 設置重試次數
    while retries > 0:
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=60)
            print(f"回應狀態碼: {response.status_code}")

            if response.status_code == 404:  # 如果到達無效頁面，退出循環
                print("已到達無效頁面，結束爬取。")
                break

            if response.status_code != 200:
                print(f"第 {current_page} 頁請求失敗")
                break

            # 解析返回數據
            data = response.json()
            articles = data.get("nodes", [])
            if not isinstance(articles, list) or not articles:
                print(f"第 {current_page} 頁無文章，結束爬取。")
                break

            # 生成單頁文件名
            page_output_file = os.path.join(output_dir, f"爬蟲資料_{current_page}.json")

            # 保存當前頁數據到文件
            with open(page_output_file, "w", encoding="utf-8") as f:
                json.dump(articles, f, ensure_ascii=False, indent=4)

            # 更新已完成的頁數
            completed_pages.append(current_page)
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump({"completed_pages": completed_pages}, f, ensure_ascii=False, indent=4)

            print(f"已保存第 {current_page} 頁的數據到文件 {page_output_file}")
            break  # 請求成功，退出重試循環
        except requests.exceptions.RequestException as e:
            print(f"第 {current_page} 頁請求錯誤: {e}")
            retries -= 1
            time.sleep(5)

    else:
        print("多次重試失敗，跳過該頁。")

    current_page += 1  # 處理下一頁

print(f"已完成所有爬取，數據保存於目錄: {output_dir}")
