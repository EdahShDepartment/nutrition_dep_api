# 會議記錄管理系統

## 專案簡介

在醫院評鑑期間，行政單位經常需要調閱過往的會議記錄，以提供佐證資料。然而，過去的做法存在許多困擾：

- 會議記錄存放在 KM 中
- 報告者需手動搜尋文件檔名、位置、打開檢查內容是否正確
- 即使找到檔案，文件內容不易快速理解，需一頁頁人工翻查

這導致：

- 評鑑前需花費大量時間整理與找檔案
- 有時即使記得大概內容，也可能找錯檔案

流程耗時又容易出現錯誤，增加同仁負擔。
本專案「會議記錄管理系統」，藉由平台來管理大量文件。基於 Python Flask 的 Web 應用程式，提供會議記錄（meeting minutes）上傳、解析、查詢、搜尋與刪除等功能。

---

## 主要功能

- 上傳 .docx 會議記錄檔案，自動解析並儲存至資料庫
- 查詢所有會議記錄與單一會議詳細內容
- 關鍵字全文搜尋會議內容
- 刪除指定會議記錄
- 提供網頁前端介面[前端 React 專案](https://github.com/ywliu-hub/meeting_system_frontend)

## 安裝步驟

1. 下載或 clone 此專案
2. 安裝依賴套件：
   ```bash
   pip install -r requirements.txt
   ```
3. 設定資料庫與環境變數（見下方）
   請在專案根目錄建立 `.env` 檔案，內容如下（以 PostgreSQL 為例）：

```
DB_HOST=localhost or VM_IP
DB_PORT=5432
DB_USER=db_user
DB_PASSWORD=db_password
DB_NAME=meeting_system
```

資料庫建立

## 啟動方式

### 開發模式

```bash
python app.py
```

預設會在 http://localhost:5003 運行。

### 正式部署

1. 執行 `wsgi.py`：
   ```bash
   python wsgi.py
   ```
2. 使用 gunicorn 啟動（Linux）：
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5003 wsgi:app
   ```

---

## 目錄結構簡介

- `app.py`：主程式，Flask API 入口
- `db_handler.py`：資料庫操作模組
- `tools/`：docx 解析工具
- `static/`會議文件資料夾
- `templates/`：HTML 模板(已廢棄，前端已改為 React)

## 專案結構

```
meeting_system_backend/
├── app.py             # 主應用程式、所有的服務、路由控制在這，未來要擴充api都是在這裡擴充(開發時可在這裡啟動 debug)
├── wsgi.py            # 正式上線時啟動wsgi server
├── db_handler.py      # DB 資料庫操作
├── requirements.txt   # 相依套件列表
├── static/            # 會議文件資料夾
├── templates/         # HTML 模板(已廢棄，前端已改為React)
└── tools/             # 工具模組
    ├── read_docx_1.py  # 抓取會議上半部(Meeting Specifics)
    ├── read_docx_2.py  # 抓取會議下半部(Meeting Minutes)
    ├── clean_content.py    # 用於清理會議內容用(沒用到)
    └── faiss_db_imp/       # 目前效果不佳(沒用到)
      ├── faiss_meeting_db   # 向量資料庫
      ├── setup_faiss_db.py  # 讀取建立向量資料庫
      └── search_helper.py   # 問答小幫手

```

## API 說明

- **prefix**:`meeting_system-api`
  在`app.py` _app.config['APPLICATION_ROOT']_ 調整

### 1. 取得所有會議記錄

- **方法**：GET
- **路徑**：`/api/get_all_meetings`
- **Query 參數**：
  - `page`（int, 選填，預設 1）：分頁頁碼
  - `page_size`（int, 選填，預設 10）：每頁筆數
- **回傳格式**：

```json
{
  "status": 200,
  "message": "success",
  "result": {
    "rows": [
      {
        "id": 1,
        "院區": "...",
        "會議名稱": "...",
        "會議主席": "...",
        "會議地點": "...",
        "會議日期": "2024-01-02",
        "會議開始時間": "13:00",
        "會議結束時間": "15:00",
        "與會人員": "...",
        "檔案路徑": "..."
      }
    ],
    "total": 100
  },
  "success": true
}
```

- **功能描述**：分頁取得所有會議記錄。
- total: 用於前端分頁用。

---

### 2. 取得單一會議及其章節內容(暫時 deprecated，改用回傳原始文件)

- **方法**：GET
- **路徑**：`/api/get_meeting`
- **Query 參數**：
  - `meeting_id`（int, 必填）：會議 ID
- **回傳格式**：

```json
{
  "status": 200,
  "message": "success",
  "result": {
    "meeting": { ... },
    "subject": [
      { "主題": "...", "內容": "..." }
    ]
  },
  "success": true
}
```

- **功能描述**：取得指定會議的詳細資料與所有章節內容。

---

### 3. 上傳 .docx 會議記錄檔案

- **方法**：POST
- **路徑**：`/api/upload_meeting_docx`
- **Body**：`multipart/form-data`
  - `file`：.docx 會議記錄檔案
- **回傳格式**：

```json
{
  "status": 200,
  "message": "file saved and inserted successfully",
  "result": "filename.docx",
  "success": true
}
```

- **功能描述**：上傳並解析 .docx 會議記錄，資料寫入資料庫。

---

### 4. 以關鍵字搜尋會議內容

- **方法**：GET
- **路徑**：`/api/meetings/search`
- **Query 參數**：
  - `keyword`（str, 必填）：搜尋關鍵字
  - `page`（int, 選填，預設 1）：分頁頁碼
  - `page_size`（int, 選填，預設 10）：每頁筆數
- **回傳格式**：

```json
{
  "status": 200,
  "message": "Search completed",
  "result": [ ... ],
  "success": true
}
```

- **功能描述**：以關鍵字搜尋所有會議內容。

---

### 5. 刪除指定會議

- **方法**：DELETE
- **路徑**：`/api/meetings/del`
- **Query 參數**：
  - `meeting_id`（int, 必填）：會議 ID
- **回傳格式**：

```json
{
  "status": 200,
  "message": "Meeting {meeting_id} deleted",
  "success": true
}
```

- **功能描述**：刪除指定的會議記錄。

---

### 6. 取得會議記錄檔案

- **方法**：GET
- **路徑**：`/api/download/<filename>`
- **路徑參數**：
  - `filename`（str, 必填）：要下載的檔案名稱（含副檔名，為 .docx）
- **回傳**：
  - 成功時：直接下載檔案（`Content-Disposition: attachment`）
  - 失敗時（檔案不存在）：

```json
{
  "status": 404,
  "error": "檔案不存在",
  "success": false
}
```

- **功能描述**：下載指定名稱的會議記錄檔案。(也用於前端檢視時)

---

## 注意事項

- 目前文件格式僅支援 .docx
- 目前上線的版本所對應的資料庫是 VM2 上的資料庫 | 暫時的版本  
  VM2 NTSHD02(10.1.207.19)->Postgre SQL->meeting_system  
  目前上線的版本**新增資料**的步驟為:

  1. 準備一個 all_minutes.xlsx(目前抓 Meeting_Minutes 是透過郭醫師使用 R 輸出 excel)
  2. 執行 upload_db.py
  3. 確認是否有 Insert 到 DB
     如果 OK 請繼續下一步驟，如果不 OK 請看常見問題
  4. 手動將該 .docx 文件放置 /static 底下
  5. 完成**新增資料**的動作

- 未來若會議下半段(Meeting_Minutes)的抓取順利  
  請使用 VM1 上的資料庫  
  VM1 NTSHD01(10.1.207.18)->Postgre SQL->meeting_system  
  此版本可以使用上傳資料的 API  
  並且 DB 也有作正規化(主檔、副檔)

## 待改善 or 待開發

1. 優化會議下半段(Meeting_Minutes)的抓取(read_docx_2.py)  
   **read_docx_2.py 必須優化**
   如果 R 較好也可使用 Python 呼叫 R 清理文件
2. 會議文件優先權排序(未確定)

## 常見問題

- Insert 失敗，請確認 excel 欄位名是否正確?要與 DB 一樣才行。
- 注意 VM1 上的 meeting_system 與 VM2 上的 schema 不同，VM1 是未來要使用的(解決會議下半段的抓取後)，VM2 上的只是暫時的。
