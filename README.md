# Resort VIP Admin API

渡假村 VIP 後台管理系統 API。

## 技術架構

* Python 3.12
* FastAPI
* SQL Server
* SQLAlchemy
* PyODBC
* Docker (規劃中)

---

## 建立虛擬環境

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

---

## 安裝套件

```bash
pip install -r requirements.txt
```

---

## 設定環境變數

建立 `.env`

```env
APP_NAME=Resort VIP Admin API
APP_ENV=local

DB_SERVER=localhost
DB_NAME=ResortVipAdminDB
DB_USER=resortmgr
DB_PASSWORD=your_password

DB_DRIVER=ODBC Driver 17 for SQL Server

FRONTEND_ORIGIN=http://localhost:5173
```

---

## 啟動系統

```bash
uvicorn app.main:app --reload --port 8000
```

啟動成功後：

API：

```text
http://localhost:8000
```

Swagger：

```text
http://localhost:8000/docs
```

---

## 專案結構

```text
app
├─ main.py
├─ config.py
├─ database.py
│
├─ routers
│  └─ employee_router.py
│
├─ services
│  └─ employee_service.py
│
├─ models
│  └─ employee_model.py
│
└─ schemas
   └─ employee_schema.py
```

---

## API

### 員工管理

取得員工清單

```http
GET /api/employees
```

---

## 資料庫

```text
Database
└─ ResortVipAdminDB
```

目前使用：

```text
dbo.Employees
```

---

## 開發版本

```text
v0.1.0
- 建立 FastAPI 專案
- 建立 MSSQL 連線
- 建立 Employee API
- 建立 Service Layer
```
