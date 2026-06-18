# 🐳 Ghid Docker - Lansare și Mentenanță

## Cerințe Prealabile

- **Docker Desktop** (sau Docker Engine + Docker Compose)
- **Versiunea**: Docker 20.10+, Docker Compose 2.0+

### Instalare:

- **Windows/Mac**: https://www.docker.com/products/docker-desktop
- **Linux**: https://docs.docker.com/engine/install/

---

## 🚀 Lansare Rapidă (3 pași)

### 1. Clonare și Navigare

```bash
# Intră în directorul Backend
cd Backend
```

### 2. Pornire Containerelor

```bash
# Pornire cu docker-compose
docker-compose up -d

# Sau, dacă vrei să vezi logs în timp real:
docker-compose up
```

### 3. Verificare Status

```bash
docker-compose ps

# Trebuie să vezi:
# - proiect_db     (PostgreSQL) - healthy ✓
# - proiect_api    (FastAPI)    - running ✓
```

**API disponibil la**: `http://localhost:8000`

---

## 🔧 Configurare

### Variabile de Mediu

Editează `.env.docker` pentru a schimba configurările:

```env
# Database
DB_USER=proiect_user
DB_PASSWORD=change_in_production
DB_NAME=proiect_db
DB_PORT=5432

# API
API_PORT=8000

# Securitate (IMPORTANT: Schimbă în producție!)
SECRET_KEY=your-secret-key-change-this
```

### Încărcare Variabilelor

```bash
# Pornire cu variabile personalizate
docker-compose --env-file .env.docker up -d
```

---

## 📦 Structura Containerelor

```
┌─────────────────────────────────────────┐
│       Docker Network: proiect_network    │
├─────────────────────────────────────────┤
│                                         │
│  ┌────────────────────┐                 │
│  │  proiect_db        │                 │
│  │  (PostgreSQL 17)   │                 │
│  │  Port: 5432        │                 │
│  │  Volume: DB Data   │                 │
│  └────────────────────┘                 │
│           │                             │
│           │ (Internal Network)          │
│           ▼                             │
│  ┌────────────────────┐                 │
│  │  proiect_api       │                 │
│  │  (FastAPI)         │                 │
│  │  Port: 8000        │                 │
│  │  (Exposed)         │                 │
│  └────────────────────┘                 │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🛑 Oprire și Curățare

### Oprire

```bash
# Oprire (păstrează datele)
docker-compose down

# Oprire + ștergere volume (ATENȚIE: pierde datele)
docker-compose down -v
```

### Logs și Debugging

```bash
# Vezi logs din API
docker-compose logs api

# Vezi logs din Database
docker-compose logs db

# Urmărire logs în timp real
docker-compose logs -f

# Logs doar din ultimele 100 rânduri
docker-compose logs --tail=100
```

---

## 🔍 Acces Database

### Din CLI

```bash
# Conectare PostgreSQL din container
docker-compose exec db psql -U proiect_user -d proiect_db

# Comenzi SQL utile:
# \dt              - listează tabelele
# \d tabelul_name  - vede structura tabelului
# \q               - ieșire
```

### Din Tool GUI

```
Host: localhost
Port: 5432
User: proiect_user
Password: proiect_password_change_in_prod
Database: proiect_db
```

Recomandări: pgAdmin, DBeaver, ou DataGrip

---

## 🔄 Migrații Database

Migrațiile se execută **automat** la pornirea containerului din:

```
supabase/migrations/
```

Fiecare fișier SQL este executat în ordine alfabetică.

### Adăugare Migrație Nouă

```bash
# 1. Creează fișier în supabase/migrations/
supabase/migrations/20260618120000_table_name.sql

# 2. Restart container-ul
docker-compose restart db
```

---

## 🏗️ Rebuild și Reconstruire

### Rebuild Aplicație (după schimbări cod)

```bash
docker-compose build --no-cache api
docker-compose up -d api
```

### Rebuild Total

```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

## ⚙️ Comenzi Utile

```bash
# Verifică versiune Docker
docker --version
docker-compose --version

# Listează toate containerele
docker ps -a

# Inspecția network
docker network ls
docker network inspect proiect_network

# Volumuri
docker volume ls
docker volume inspect backend_postgres_data

# Ștergere imagini inutile
docker image prune -a

# Curățare completă (ATENȚIE: pierde totul)
docker system prune -a --volumes
```

---

## 🐛 Troubleshooting

### 1. **Port deja în folosință**

```bash
# Schimbă porturi în .env.docker
DB_PORT=5433
API_PORT=8001
```

### 2. **Container nu pornește**

```bash
# Vezi eroarea
docker-compose logs api

# Rebuild și restart
docker-compose build --no-cache
docker-compose up -d
```

### 3. **Database nu e gata**

```bash
# Verifică health
docker-compose ps

# Așteptă healthcheck (max 25 secunde)
# Apoi restart API:
docker-compose restart api
```

### 4. **Schimbă parola Database**

```bash
# ATENTIE: Pierde datele existente
docker-compose down -v
# Editează DB_PASSWORD în .env.docker
docker-compose up -d
```

---

## 📋 Checklist Producție

- [ ] Schimbă `SECRET_KEY` cu valoare sigură (minim 32 caractere)
- [ ] Schimbă `DB_PASSWORD` cu parolă complexă
- [ ] Setează `DEBUG=false`
- [ ] Configurează `SUPABASE_URL` corect dacă e nevoie
- [ ] Configurează backup-uri automate pentru PostgreSQL
- [ ] Setează resurse (CPU/RAM limits) în docker-compose
- [ ] Configurează monitoring/logging centralizat
- [ ] Testează disaster recovery (restaurare din backup)

---

## 🔐 Securitate

### Variabile Sensibile

**NU comita `.env.docker` în Git!**

```bash
echo ".env.docker" >> .gitignore
```

### În Producție

```bash
# Folosește Docker Secrets
# Sau: Docker Swarm / Kubernetes
# Sau: Variabile de mediu din sistem host
```

---

## 📖 Resurse Adiționale

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

**Data Document**: 2026-06-18  
**Status**: Ready for Development & Production
