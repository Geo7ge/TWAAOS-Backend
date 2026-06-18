# Proiect Backend API

Structura profesională pentru un proiect backend FastAPI cu:

- **Supabase** (PostgreSQL + Auth)
- JWT Authentication
- User Management
- CORS Middleware
- Testing cu Pytest

## 📁 Structura de fișiere

```
Backend/
├── main.py                 # Entry point al aplicației
├── config.py              # Configurare + variabile de mediu
├── database.py            # Setup SQLAlchemy și session
├── requirements.txt       # Dependencies
├── .env.example          # Template variabile mediu
│
├── models/               # SQLAlchemy ORM models
│   ├── __init__.py
│   └── user.py
│
├── schemas/              # Pydantic validation models
│   ├── __init__.py
│   └── user.py
│
├── routes/               # API endpoints routers
│   ├── __init__.py
│   └── user_routes.py
│
├── services/             # Business logic
│   ├── __init__.py
│   └── user_service.py
│
└── tests/                # Tests
    ├── __init__.py
    └── test_api.py
```

## 🚀 Setup

1. **Creează `.env` din template:**

   ```bash
   cp .env.example .env
   ```

   Editează `.env` cu valorile tale Supabase (SUPABASE_URL și SUPABASE_KEY)

2. **Instaleaza dependentele:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Rulează aplicația:**

   ```bash
   python main.py
   ```

   Sau cu Uvicorn direct:

   ```bash
   uvicorn main:app --reload
   ```

4. **Accesează API:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📝 API Endpoints

### Users

- `POST /users/register` - Înregistrare utilizator
- `POST /users/login` - Login și obținere token
- `GET /users/{user_id}` - Get user by ID

### Health

- `GET /health` - Health check
- `GET /` - Root endpoint

## 🧪 Tests

```bash
pytest tests/
```

## 📦 Dependencies

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Supabase** - Database ORM și Auth
- **Pydantic** - Data validation
- **python-jose** - JWT
- **passlib** - Password hashing
- **pytest** - Testing framework
