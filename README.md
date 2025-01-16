# README

## 簡介 (Overview)

此程式旨在自動化部署 Google Cloud Compute Engine 實例並在其中運行 Docker 容器進行 LDA（Latent Dirichlet Allocation）主題分析。該程式使用 PySpark 和 TF-IDF 分析文本數據，並可視化主題之間的關係網絡。

## 功能 (Features)

### Google Cloud Compute Engine 集成：
- 自動創建並配置 GCP 實例。
- 配置防火牆規則以允許 SSH 訪問。

### Docker 集成：
- 拉取指定的 Docker 鏡像（預設為 `python:3.12.3`）。
- 在實例中執行 LDA 分析容器。

### LDA 主題分析：
- 使用結巴分詞進行中文文本處理。
- 計算最佳主題數量（基於困惑度）。
- 打印每個主題的關鍵詞。

### 主題可視化：
- 使用 NetworkX 和 Matplotlib 繪製主題關係網絡圖。
- 使用 Louvain 方法進行社區檢測。

---

## 安裝要求 (Prerequisites)

### 軟件需求：
- Python 3.12.3 或更新版本。
- 安裝必要的庫：
  ```bash
  pip install pyspark pandas numpy matplotlib networkx python-louvain jieba
  ```
- 安裝 Google Cloud SDK 並進行身份驗證：
  ```bash
  gcloud auth login
  gcloud config set project [YOUR_PROJECT_ID]
  ```

### 數據文件：
- 一個包含 `title` 和 `body` 列的 CSV 文件（如：`/home/rrrrryeedie/final_sorted_output.csv`）。
- 一個包含停用詞的文本文件（如：`/home/rrrrryeedie/stopwords.txt`）。

---

## 使用說明 (Usage)

### 1. 配置參數
在程式的 `main()` 函數中，根據需求調整以下變數：
- `project_id`：Google Cloud 專案 ID。
- `instance_name`：Compute Engine 實例名稱。
- `zone`：實例所在的 GCP 區域。
- `docker_image`：Docker 鏡像名稱（預設為 `python:3.12.3`）。
- `csv_path`：LDA 分析的輸入 CSV 文件路徑。
- `stopwords_path`：停用詞文本文件的路徑。

### 2. 運行程式
執行程式：
```bash
python gcloud_lda_visualization.py
```

### 3. 輸出結果

#### LDA 分析結果：
- 打印每個主題的關鍵詞列表。
- 顯示基於困惑度的最佳主題數量。

#### 主題可視化：
- 生成主題相似度網絡圖，並標示社區結構。

---

## 注意事項 (Notes)

### GCloud 問題：
- 確保已經使用 `gcloud auth login` 完成身份驗證。
- 正確設置專案 ID：`gcloud config set project [PROJECT_ID]`。

### Docker 問題：
- 確保 Docker 鏡像可用。如遇權限問題，請執行 `docker login`。

### 文件路徑：
- 請確保 CSV 文件和停用詞文件的路徑正確。

---

## 英文版 (English Version)

### Overview
This script automates the deployment of a Google Cloud Compute Engine instance with Docker to perform Latent Dirichlet Allocation (LDA) topic modeling using PySpark.

### Features

#### Google Cloud Integration:
- Automatically configures a GCP Compute Engine instance.
- Sets up firewall rules for SSH access.

#### Docker Integration:
- Pulls and runs a Docker image (`python:3.12.3`).
- Executes the LDA analysis on the cloud instance.

#### LDA Analysis:
- Tokenizes Chinese text with Jieba.
- Computes optimal topics based on perplexity.
- Prints top terms for each topic.

#### Visualization:
- Generates a topic similarity network graph with NetworkX and Matplotlib.
- Performs community detection using the Louvain method.

---

## Prerequisites

### Software:
- Python 3.12.3 or later.
- Required Python libraries:
  ```bash
  pip install pyspark pandas numpy matplotlib networkx python-louvain jieba
  ```

### Files:
- CSV file containing `title` and `body` columns (e.g., `/home/rrrrryeedie/final_sorted_output.csv`).
- Stopwords text file (e.g., `/home/rrrrryeedie/stopwords.txt`).

---

## Usage

### 1. Configure Parameters
Adjust the following variables in the `main()` function as needed:
- `project_id`: Google Cloud Project ID.
- `instance_name`: Compute Engine instance name.
- `zone`: GCP zone for the instance.
- `docker_image`: Docker image name (default: `python:3.12.3`).
- `csv_path`: Path to the input CSV file for LDA analysis.
- `stopwords_path`: Path to the stopwords text file.

### 2. Run the Script
Execute the script:
```bash
python gcloud_lda_visualization.py
```

### 3. Output

#### LDA Analysis Results:
- Prints the top keywords for each topic.
- Displays the optimal number of topics based on perplexity.

#### Visualization:
- Generates a topic similarity network graph and marks community structures.

---

## Notes

### GCloud Issues:
- Ensure you have completed authentication with `gcloud auth login`.
- Set the correct project ID with `gcloud config set project [PROJECT_ID]`.

### Docker Issues:
- Ensure the Docker image is available. If permission issues arise, run `docker login`.

### File Paths:
- Ensure the CSV file and stopwords file paths are correct.
