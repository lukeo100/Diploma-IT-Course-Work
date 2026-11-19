# DOCS

This document explains how the project is designed and why. Line by line detail lives in the code comments.

## 1. Overview

The project is one small API (students and courses) built two ways against the same Supabase PostgreSQL database.
Version 1 writes SQL by hand. Version 2 lets SQLAlchemy generate the SQL from Python classes. Building both
makes the trade-offs easy to see.

Request flow, for both versions:

```
Client (Swagger UI / pytest)
   -> FastAPI route function
   -> database layer (psycopg raw SQL  |  SQLAlchemy session)
   -> Supabase PostgreSQL (schema: fastapi_practice)
   -> JSON response
```

## 2. Database

### Why a separate schema
Your Learning project's `public` schema is shared by many exercises. These tables live in their own schema,
`fastapi_practice`, so they cannot clash with anything else. Code refers to them as `fastapi_practice.students`.

### Tables

| Table | Column | Type | Notes |
|---|---|---|---|
| courses | id | integer | auto-generated identity, primary key |
| courses | name | varchar(100) | required |
| students | id | integer | auto-generated identity, primary key |
| students | name | varchar(100) | required |
| students | course_id | integer | required, foreign key to `courses.id` |

One course has many students (one-to-many). The foreign key means the database itself refuses a student whose
`course_id` does not exist, and refuses to delete a course that still has students.

Seed data: courses 1 to 4 (Programming, Networking, Cyber Security, Web Development) and 8 students, two per course.

### Files
- `sql/schema.sql` drops and recreates the schema's tables and seed data. It was applied to Supabase as the
  migration `fastapi_practice_schema`.
- `sql/reset.sql` only restores the data (`TRUNCATE ... RESTART IDENTITY` then re-insert). Tests use it.

## 3. Configuration and secrets

`.env` holds one variable, `DATABASE_URL`, using the Supabase Session pooler:

```
postgresql+psycopg://postgres.<project-ref>:<password>@aws-0-ap-southeast-2.pooler.supabase.com:5432/postgres?sslmode=require
```

- `postgresql+psycopg://` is the SQLAlchemy form: "PostgreSQL, using the psycopg driver".
- Plain psycopg only accepts `postgresql://`, so v1 removes the `+psycopg` before connecting.
- `python-dotenv` loads the file at start up. `.env` is listed in `.gitignore` so the password is never committed.
  `.env.example` is the safe template to share.
- The direct connection (`db.<project-ref>.supabase.co`) is IPv6 only, so it fails on IPv4 only networks. The Session pooler works on both, and in session mode (port 5432) it behaves like a normal connection. The direct string is kept commented out in `.env`.

## 4. Version 1: Psycopg and raw SQL (`v1_psycopg/main.py`)

Key ideas:

- **One connection per request.** `get_connection()` opens a connection, and a `with` block closes it. The `with`
  block also commits on success and rolls back if an exception is raised.
- **`dict_row`.** Rows come back as dictionaries, which FastAPI turns into JSON with no extra work.
- **Parameterised queries.** Values are passed separately (`%s` placeholders and a tuple). The database never
  treats them as SQL, which is what prevents SQL injection. User input is never put into the SQL string.
  The only f-string value is the fixed schema name, which is not user input.
- **`RETURNING`.** INSERT, UPDATE and DELETE return the affected row in the same statement, so no second query.
- **`fetchone()` vs `fetchall()`.** `fetchone()` gives one row or `None` (used for 404 checks). `fetchall()` gives a list.
- **JOIN.** `GET /students` joins students to courses so the response shows the course name under `course`.
- **Simple parameters.** `name` and `course_id` on POST and PUT are plain function parameters, so FastAPI reads
  them from the query string. There is no Pydantic model in v1.
- **Errors.** No matching row means `None`, which becomes a 404. A foreign key violation from the database is
  caught and returned as a 400.

## 5. Version 2: SQLAlchemy ORM (`v2_orm/`)

| File | Job |
|---|---|
| `database.py` | Loads `.env`, creates the **engine** (connection pool) and the **session factory**, and defines `get_db()` |
| `models.py` | **ORM classes** `Course` and `Student` that map to the existing tables |
| `schemas.py` | **Pydantic classes** that describe the JSON going in and out |
| `main.py` | The routes |

Key ideas:

- **Engine and session.** The engine is the connection to the database, created once. A session is a short-lived
  workspace that tracks objects and changes. `get_db()` gives every request its own session and closes it afterwards.
  FastAPI supplies it with `Depends(get_db)` (dependency injection).
- **Models are not migrations.** The tables already exist, so the app never calls `Base.metadata.create_all()`.
  The models only describe the tables so SQLAlchemy can query them. Names, types and the foreign key must match.
- **Two kinds of model.** ORM models (`models.py`) represent database rows. Pydantic schemas (`schemas.py`)
  represent API input and output. Keeping them separate means the API shape can change without changing the
  database, and the reverse.
- **Relationships.** `Course.students` and `Student.course` are linked with `back_populates`.
  `student.course.name` reads the course name with no hand-written JOIN.
- **The unit of work.**
  - `db.add(obj)` stages a new object.
  - `db.commit()` sends the changes to the database and makes them permanent.
  - `db.refresh(obj)` reloads the object, which fills in database-generated values such as the new `id`.
  - `db.get(Model, id)` finds a row by primary key, or `None`.
  - `db.delete(obj)` stages a delete.
- **Updating** is just changing attributes on a loaded object, then committing. The session detects the change.
- **Loading strategy.** `selectinload` fetches all needed courses in one extra query instead of one per student
  (the "N+1" problem).
- **Delete detail.** The response is built before deleting, because a deleted object cannot be read afterwards.

## 6. Comparing the two

| | v1 raw SQL | v2 ORM |
|---|---|---|
| You write | SQL strings | Python classes and method calls |
| Result of a query | dict | Python object |
| Joins | written by hand | through `relationship()` |
| Input validation | none beyond types | Pydantic models |
| Schema knowledge | lives in the SQL | duplicated in `models.py`, must be kept in sync |
| Control over SQL | full | indirect |
| Boilerplate | low for small apps | higher up front, lower as the app grows |

Both return identical JSON, which is why one test file can check both.

## 7. API behaviour

| Endpoint | Success | Errors |
|---|---|---|
| `GET /database` (v1) | 200, `{"database": "postgres"}` | |
| `GET /courses` | 200, list ordered by id | |
| `GET /students` | 200, `[{id, name, course}]` | |
| `GET /students/{id}` | 200, `{id, name, course}` | 404 not found |
| `POST /students` | 201, `{id, name, course_id}` | 400 unknown course |
| `PUT /students/{id}` | 200, `{id, name, course_id}` | 404 not found, 400 unknown course |
| `DELETE /students/{id}` | 200, the deleted row | 404 not found |

## 8. Tests

- `tests/conftest.py` provides three things: an environment check, an automatic database reset around every test,
  and an `api` fixture that runs each test against v1 and then v2.
- `tests/test_api.py` covers every endpoint, the 404 and 400 cases, and the Avery Johnson sequence from the task
  pages (create in course 1, move to course 3, delete, confirm 404).
- `tests/test_v1_database.py` covers `GET /database`, which only v1 has.
- `TestClient` calls the app in memory, so no server needs to be running. The database is real, so tests need
  your password in `.env` and a working connection.

## 9. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `password authentication failed` | wrong password, or special characters not URL-encoded |
| `failed to resolve host` or network unreachable | using the direct host without IPv6, use the Session pooler string |
| `Tenant or user not found` | pooler username must be `postgres.<project-ref>`, not just `postgres` |
| `relation "fastapi_practice.students" does not exist` | schema not applied, run `sql/schema.sql` |
| `Put your real database password in .env` | the placeholder is still in `.env` |
| `fastapi: command not found` | venv not activated, or `fastapi[standard]` not installed |
| `Address already in use` | the other version is still running on port 8000 |

## 10. Concepts worth being able to explain

- Why parameterised queries stop SQL injection
- What `RETURNING` does and why it saves a query
- Difference between a Pydantic model and an SQLAlchemy model
- What an engine, a session and a commit each do
- What `relationship()` and `back_populates` give you
- Lazy loading versus `selectinload`
- Why the ORM version never calls `create_all()`
