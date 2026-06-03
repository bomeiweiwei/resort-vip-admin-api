# Resort VIP Admin API

渡假村 VIP 後台管理系統 API，基於 FastAPI 與 SQL Server 構建。

## Tech Stack

| 項目 | 版本 |
|------|------|
| Python | 3.12 |
| FastAPI | 0.136 |
| SQLAlchemy | 2.0 |
| SQL Server | — |
| PyODBC | 5.3 |
| python-jose (JWT) | 3.5 |
| passlib / bcrypt | — |

---

## Getting Started

### 1. 建立虛擬環境

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. 安裝套件

```bash
pip install -r requirements.txt
```

### 3. 設定環境變數

建立 `.env`：

```env
APP_NAME=Resort VIP Admin API
APP_ENV=local

DB_SERVER=localhost
DB_NAME=ResortVipAdminDB
DB_USER=resortmgr
DB_PASSWORD=your_password
DB_DRIVER=ODBC Driver 17 for SQL Server

FRONTEND_ORIGIN=http://localhost:5173

JWT_SECRET_KEY=change_this_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. 啟動開發伺服器

```bash
uvicorn app.main:app --reload --port 8000
```

| 端點 | URL |
|------|-----|
| API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

---

## Project Structure

```
app/
├── main.py              # FastAPI 應用入口、CORS、路由註冊
├── config.py            # 環境變數設定（Settings singleton）
├── database.py          # SQLAlchemy engine、Session、get_db 依賴
│
├── routers/             # 路由層（薄層，僅做請求轉發）
│   ├── auth_router.py
│   └── employee_router.py
│
├── services/            # 業務邏輯層
│   ├── auth_service.py
│   └── employee_service.py
│
├── models/              # SQLAlchemy ORM 模型（對應 DB 資料表）
│   └── employee_model.py
│
├── schemas/             # Pydantic 請求 / 回應結構
│   ├── auth_schema.py
│   └── employee_schema.py
│
└── utils/
    └── security.py      # bcrypt 雜湊、JWT 產生
```

---

## API

### Auth

| Method | Path | 說明 |
|--------|------|------|
| POST | `/api/auth/login` | 員工登入，回傳 JWT |

**Login Request**
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Login Response**
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "employee_id": 1,
  "employee_code": "EMP001",
  "employee_name": "王小明",
  "email": "user@example.com",
  "role": "admin"
}
```

### 員工管理

| Method | Path | 說明 |
|--------|------|------|
| GET | `/api/employees` | 取得員工清單 |

---

## Database

```
ResortVipAdminDB
└── dbo.Employees
```

| 欄位 | 類型 | 說明 |
|------|------|------|
| EmployeeId | int | PK |
| EmployeeCode | varchar(20) | 員工編號 |
| EmployeeName | varchar(50) | 姓名 |
| Email | varchar(100) | 登入帳號 |
| PasswordHash | varchar(255) | bcrypt 雜湊 |
| Role | varchar(30) | 角色權限 |
| Department | varchar(50) | 部門（可為空） |
| IsActive | bit | 帳號狀態 |
| LastLoginAt | datetime | 最後登入時間 |
| CreatedAt | datetime | 建立時間 |
| UpdatedAt | datetime | 更新時間 |

---

## Changelog

### v0.1.0
- 建立 FastAPI 專案架構
- 建立 MSSQL 連線（SQLAlchemy + PyODBC）
- 員工管理 API
- Service Layer 分層設計
- JWT 驗證模組
