# Resort VIP Admin API

渡假村 VIP 後台管理系統 API，基於 FastAPI 與 SQL Server 構建，整合可插拔 AI 提供者層，支援 VIP 賓客入住與行程智慧推薦。

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
| LangChain | — |

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

建立 `.env`（可參考 `.env.example`）：

```env
APP_NAME=Resort VIP Admin API
APP_ENV=local

DB_SERVER=localhost
DB_NAME=ResortVipAdminDB
DB_USER=resortmgr
DB_PASSWORD=your_password
DB_DRIVER=ODBC Driver 18 for SQL Server

FRONTEND_ORIGIN=http://localhost:5173
VIP_FRONTEND_URL=http://localhost:5174

JWT_SECRET_KEY=change_this_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# RAG / Embedding（僅支援 Azure OpenAI）
VECTOR_DB_DIR=/vector_db/resort_knowledge_faiss
EMBEDDING_PROVIDER=azure
AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# AI 提供者：azure | lmstudio | gemini | ollama
AI_PROVIDER=azure

# Azure OpenAI
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_BASE_URL=
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5.1

# LM Studio（本地）
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_API_KEY=lm-studio
LMSTUDIO_MODEL_NAME=

# Gemini
GEMINI_API_KEY=
GEMINI_MODEL_NAME=gemini-3.5-flash

# Ollama（本地）
OLLAMA_MODEL_NAME=
OLLAMA_BASE_URL=http://localhost:11434
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

## Docker

```bash
docker build -t resort-vip-admin-api .
docker run -p 8000:8000 --env-file .env resort-vip-admin-api
```

映像基於 `python:3.12-slim`，已內建安裝 Microsoft ODBC Driver 18 for SQL Server。

---

## Project Structure

```
app/
├── main.py                      # FastAPI 應用入口、CORS、路由註冊
├── config.py                    # 環境變數設定（Settings singleton）
├── database.py                  # SQLAlchemy engine、Session、get_db 依賴
│
├── routers/                     # 路由層（薄層，僅做請求轉發）
│   ├── auth_router.py
│   ├── employee_router.py
│   ├── checkin_router.py
│   └── recommend_router.py
│
├── services/                    # 業務邏輯層
│   ├── auth_service.py
│   ├── employee_service.py
│   ├── checkin_service.py
│   ├── recommend_service.py
│   ├── itinerary_recommendation_service.py
│   ├── itinerary_knowledge_service.py   # RAG 知識檢索
│   └── vip_prompt_service.py            # VIP Prompt 組裝
│
├── models/                      # SQLAlchemy ORM 模型（對應 DB 資料表）
│   ├── employee_model.py
│   ├── customer_model.py
│   ├── customer_vip_account_model.py
│   ├── room_model.py
│   ├── booking_stay_model.py
│   ├── vip_itinerary_recommendation_model.py
│   └── vip_itinerary_schedule_model.py
│
├── schemas/                     # Pydantic 請求 / 回應結構
│   ├── auth_schema.py
│   ├── employee_schema.py
│   ├── checkin_schema.py
│   └── recommend_schema.py
│
├── ai/                          # 可插拔 AI 提供者層
│   ├── base.py                  # BaseAILangchain 介面
│   ├── factory.py               # create_ai_langchain() 工廠
│   ├── embedding_factory.py     # get_embedding_function()（Azure OpenAI）
│   ├── gemini_langchain.py
│   ├── azure_langchain.py
│   ├── lmstudio_langchain.py
│   └── ollama_langchain.py
│
├── prompts/
│   └── prompt_builder.py        # LangChain Prompt 組裝
│
├── enums/
│   └── ai_type.py               # AiType 列舉
│
└── utils/
    ├── security.py              # bcrypt 雜湊、JWT 產生
    ├── account_generator.py
    └── date_helper.py
```

---

## API

所有需要驗證的端點須在 `Authorization` header 帶入 `Bearer <token>`。

### Auth

| Method | Path | 驗證 | 說明 |
|--------|------|------|------|
| POST | `/api/auth/login` | — | 員工登入，回傳 JWT |

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

| Method | Path | 驗證 | 說明 |
|--------|------|------|------|
| GET | `/api/employees` | 需要 | 取得員工清單 |

### VIP 入住管理

| Method | Path | 驗證 | 說明 |
|--------|------|------|------|
| GET | `/api/checkins/room-types` | 需要 | 取得房型清單 |
| GET | `/api/checkins/rooms?room_type_id={id}` | 需要 | 依房型取得房間清單 |
| POST | `/api/checkins` | 需要 | 建立入住紀錄 |
| POST | `/api/checkins/{customer_id}/generate-recommendation` | 需要 | 為指定賓客產生 AI 行程推薦 |

### AI 行程推薦

| Method | Path | 驗證 | 說明 |
|--------|------|------|------|
| GET | `/api/recommends/itinerary` | 需要 | 取得所有行程推薦紀錄 |
| GET | `/api/recommends/itinerary/{customer_id}/{recommendation_id}/schedules` | 需要 | 取得推薦的行程明細 |

---

## AI 提供者

透過環境變數 `AI_PROVIDER` 切換，無需修改程式碼：

| 值 | 提供者 | 所需環境變數 |
|----|--------|-------------|
| `azure` | Azure OpenAI | `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_BASE_URL`, `AZURE_OPENAI_DEPLOYMENT_NAME` |
| `lmstudio` | LM Studio（本地） | `LMSTUDIO_BASE_URL`, `LMSTUDIO_API_KEY`, `LMSTUDIO_MODEL_NAME` |
| `gemini` | Google Gemini | `GEMINI_API_KEY`, `GEMINI_MODEL_NAME` |
| `ollama` | Ollama（本地） | `OLLAMA_MODEL_NAME`, `OLLAMA_BASE_URL` |

## Embedding 提供者

透過環境變數 `EMBEDDING_PROVIDER` 設定，目前僅支援 Azure OpenAI：

| 值 | 提供者 | 所需環境變數 |
|----|--------|-------------|
| `azure` | Azure OpenAI Embeddings | `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_BASE_URL`, `AZURE_OPENAI_EMBEDDING_MODEL` |

FAISS 索引須在啟動前預先建置並放置於 `VECTOR_DB_DIR` 指定的路徑。

---

## Database

```
ResortVipAdminDB
├── dbo.Employees
├── dbo.Customers
├── dbo.CustomerVipAccounts
├── dbo.Rooms
├── dbo.BookingStays
├── dbo.ResortKnowledgeItem
├── dbo.VipItineraryRecommendations
└── dbo.VipItinerarySchedules
```

### dbo.Employees

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

### v0.5.0
- 移除 HuggingFace embedding 支援，統一改用 Azure OpenAI Embeddings
- 將所有 `os.getenv()` 呼叫集中至 `Settings` singleton（`config.py`）
- 新增 `EMBEDDING_PROVIDER`、`AZURE_OPENAI_EMBEDDING_MODEL`、`VECTOR_DB_DIR`、`VIP_FRONTEND_URL` 至 Settings

### v0.4.0
- 新增行程推薦讀取端點（清單 / 明細）

### v0.3.0
- 整合 RAG 知識檢索，根據賓客資料產生 VIP 行程推薦
- 入住端點加入驗證保護

### v0.2.0
- 可插拔 AI 提供者層（Gemini / Azure OpenAI / LM Studio / Ollama）
- 行程推薦產生端點
- VIP 入住管理 API

### v0.1.0
- 建立 FastAPI 專案架構
- 建立 MSSQL 連線（SQLAlchemy + PyODBC）
- 員工管理 API
- Service Layer 分層設計
- JWT 驗證模組
