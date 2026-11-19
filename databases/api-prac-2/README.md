# FastAPI + Supabase practice (api-prac-2)

A small students and courses API built twice, to compare the two approaches from the course tasks:

| Folder | Approach | Task page |
|---|---|---|
| `v1_psycopg/` | Psycopg 3 with raw SQL, no ORM | Database connection |
| `v2_orm/` | SQLAlchemy ORM (Psycopg 3 is the driver underneath) | ORM |

Both talk to the same Supabase tables and return the same JSON. For the full explanation see [DOCS.md](DOCS.md).

## Project layout

```
api-prac-2/
├── v1_psycopg/main.py      raw SQL version (single file)
├── v2_orm/                 ORM version: database.py, models.py, schemas.py, main.py
├── sql/schema.sql          creates the tables and seed data (already applied to Supabase)
├── sql/reset.sql           puts the data back to the seed state (used by the tests)
├── tests/                  pytest tests, run against both versions
├── .env                    your database connection string (NOT committed)
├── .env.example            template for .env
├── requirements.txt
└── setup.sh                creates the virtual environment
```

## 1. Set up the environment

Run these in the project folder on your Mac:

```bash
./setup.sh                    # creates .venv and installs requirements.txt
source .venv/bin/activate
```

Manual equivalent: `python3 -m venv .venv`, activate it, then `pip install -r requirements.txt`.

## 2. Add your database password

Open `.env` and replace `YOUR_DB_PASSWORD` with your Supabase database password
(Dashboard > Project Settings > Database). URL-encode special characters (`@` becomes `%40`).

`.env` uses the Supabase **Session pooler** (IPv4 friendly, port 5432). The direct connection is IPv6 only and
fails with "failed to resolve host" on networks without IPv6. The direct string is kept commented out in `.env`.

## 3. Run an API

From the project root (run one at a time, they both use port 8000):

```bash
fastapi dev v1_psycopg/main.py     # version 1
fastapi dev v2_orm/main.py         # version 2
```

Open http://127.0.0.1:8000/docs for Swagger UI and try the endpoints.

## 4. Run the tests

```bash
pytest -v
```

The tests use the real Supabase database. Before and after each test, `sql/reset.sql` restores the seed data,
so your tables are left clean. Only the `fastapi_practice` schema is touched. Every test runs against both versions.

## Endpoints

| Method | Path | v1 input | v2 input |
|---|---|---|---|
| GET | `/database` | none | not in v2 |
| GET | `/courses` | none | none |
| GET | `/students` | none | none |
| GET | `/students/{id}` | none | none |
| POST | `/students` | query: `name`, `course_id` | JSON body |
| PUT | `/students/{id}` | query: `name`, `course_id` | JSON body |
| DELETE | `/students/{id}` | none | none |

Errors: `404` when a student does not exist, `400` when `course_id` points at a course that does not exist.

## Resetting the database

Data only: run `sql/reset.sql` in the Supabase SQL Editor.
Tables and data: run `sql/schema.sql` (it drops and recreates both tables).
