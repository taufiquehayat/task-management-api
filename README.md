# 📝 Task Management API

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![JWT](https://img.shields.io/badge/Auth-JWT-black?logo=jsonwebtokens)

A secure RESTful Task Management API built with **FastAPI, PostgreSQL, SQLAlchemy, and JWT Authentication**.

Users can register, log in, and manage their own tasks. Every task is tied to a user, so **one user can never see or modify another user's tasks**.

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Running the App](#-running-the-app)
- [API Endpoints](#-api-endpoints)
- [Usage Examples](#-usage-examples)
- [Authentication Flow](#-authentication-flow)
- [Database Schema](#-database-schema)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## ✨ Features

- 🔐 User registration and login
- 🔑 Password hashing with **Bcrypt**
- 🪪 **JWT-based** authentication (Bearer token)
- ✅ Full task CRUD (create, read, update, delete)
- 👤 User-specific task access (ownership enforced)
- 🐘 PostgreSQL integration through SQLAlchemy ORM
- 📚 Auto-generated interactive docs (Swagger UI)

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Auth | JWT (JSON Web Token) |
| Password Hashing | Passlib (Bcrypt) |
| Config | Python-dotenv |

---

## 📂 Project Structure

```text
task-management/
├── main.py            # App entry point, routes, models, auth logic
├── requirements.txt   # Python dependencies
├── .env               # Environment variables (not committed)
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL installed and running
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/taufiquehayat/YOUR_REPO_NAME.git

# 2. Go to the project folder
cd task-management

# 3. Create a virtual environment
python -m venv env

# 4. Activate it
# Windows:
env\Scripts\activate
# macOS / Linux:
source env/bin/activate

# 5. Install dependencies
pip install -r requirements.txt
```

---

## 🔧 Environment Variables

Create a `.env` file in the project root:

```env
algorithm=HS256
secret_key=YOUR_SECRET_KEY
db_connection=postgresql://username:password@localhost:5432/your_db_name
```

| Variable | Description |
|---|---|
| `algorithm` | JWT signing algorithm (e.g. `HS256`) |
| `secret_key` | Long random string used to sign tokens |
| `db_connection` | PostgreSQL connection string |

> 💡 Generate a strong secret key:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

> ⚠️ **Never commit your `.env` file or expose your secret key on GitHub.** Make sure `.env` is listed in `.gitignore`.

---

## ▶️ Running the App

```bash
fastapi dev main.py
```

Then open the interactive docs:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## 📡 API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|:---:|---|
| POST | `/register` | ❌ | Register a new user |
| POST | `/login` | ❌ | Log in and receive a JWT |
| GET | `/secure` | ✅ | Test protected route |
| POST | `/create_task` | ✅ | Create a new task |
| GET | `/get_task` | ✅ | Get all tasks of the logged-in user |
| GET | `/get_task/{task_id}` | ✅ | Get a specific task |
| PUT | `/update/{task_id}` | ✅ | Update a task |
| DELETE | `/task_delete/{task_id}` | ✅ | Delete a task |

---

## 🧪 Usage Examples

> Request/response bodies below are illustrative. Check `/docs` for the exact schema of your version.

**Register**

```bash
curl -X POST http://127.0.0.1:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "taufique", "password": "strongpassword"}'
```

**Login**

```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "taufique", "password": "strongpassword"}'
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Create a task (with token)**

```bash
curl -X POST http://127.0.0.1:8000/create_task \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Finish README", "description": "Polish the project docs"}'
```

**Get all tasks**

```bash
curl http://127.0.0.1:8000/get_task \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🔐 Authentication Flow

```text
Register  ->  Login  ->  Receive JWT  ->  Send JWT in Authorization header  ->  Access protected routes
```

1. The user registers; the password is hashed with Bcrypt before storing.
2. On login, the server verifies the password and issues a signed JWT.
3. The client sends `Authorization: Bearer <token>` with each protected request.
4. The server decodes the token, identifies the user, and returns only that user's data.

In Swagger UI, click **Authorize** and paste your token to test protected endpoints.

---

## 🗄 Database Schema

| Table | Purpose |
|---|---|
| `users` | Stores user details and hashed passwords |
| `task` | Stores tasks, each linked to a user |

```text
users (1) ──────< (many) task
```

---

## 🔮 Future Improvements

- [ ] Response models (Pydantic) for all endpoints
- [ ] Task status validation (e.g. `pending`, `in_progress`, `completed`)
- [ ] Pagination and filtering
- [ ] Modular project structure (routers, models, schemas, services)
- [ ] Automated testing (pytest)

---

## 👨‍💻 Author

**Taufique Hayat**

GitHub: [@taufiquehayat](https://github.com/taufiquehayat)

---

⭐ If you found this project useful, consider giving it a star!
