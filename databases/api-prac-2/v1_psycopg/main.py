"""
Version 1: FastAPI + Psycopg 3 with raw SQL (no ORM).

Run from the project root:
    fastapi dev v1_psycopg/main.py
Swagger UI: http://127.0.0.1:8000/docs
"""
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from psycopg.rows import dict_row

# Load DATABASE_URL from the .env in the project root (one folder above this file).
# The password lives in .env, never in the code.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Check your .env file.")

# .env uses the SQLAlchemy style scheme "postgresql+psycopg://".
# Plain psycopg only understands "postgresql://", so we strip the "+psycopg".
DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg://", "postgresql://", 1)

# Our tables live in their own schema, so every query names it explicitly.
SCHEMA = "fastapi_practice"

app = FastAPI(title="Students API (v1: Psycopg, raw SQL)")


def get_connection() -> psycopg.Connection:
    """Open a new connection. row_factory=dict_row makes each row a dict
    ({"id": 1, "name": "..."}) instead of a tuple, which FastAPI can return as JSON."""
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


@app.get("/database")
def get_database_name():
    """Task 1: prove the connection works by asking Postgres for the database name."""
    # "with" closes the connection for us and commits if no error happened.
    with get_connection() as conn:
        row = conn.execute("SELECT current_database() AS database").fetchone()
    return row


@app.get("/courses")
def list_courses():
    """Task 2: all courses, ordered by id."""
    with get_connection() as conn:
        # fetchall() returns a list of dicts (thanks to dict_row)
        return conn.execute(
            f"SELECT id, name FROM {SCHEMA}.courses ORDER BY id"
        ).fetchall()


@app.get("/students")
def list_students():
    """Task 3: all students, with the course NAME (not course_id) under the key "course"."""
    with get_connection() as conn:
        # JOIN: for each student, find the course row whose id matches student.course_id.
        # "c.name AS course" renames the column so the JSON key is "course".
        return conn.execute(
            f"""
            SELECT s.id, s.name, c.name AS course
            FROM {SCHEMA}.students s
            JOIN {SCHEMA}.courses c ON c.id = s.course_id
            ORDER BY s.id
            """
        ).fetchall()


@app.get("/students/{student_id}")
def get_student(student_id: int):
    """Task 3: one student. 404 if the id does not exist."""
    with get_connection() as conn:
        # %s is a placeholder. psycopg sends the value separately from the SQL text,
        # which prevents SQL injection. NEVER build the query with an f-string and user input.
        student = conn.execute(
            f"""
            SELECT s.id, s.name, c.name AS course
            FROM {SCHEMA}.students s
            JOIN {SCHEMA}.courses c ON c.id = s.course_id
            WHERE s.id = %s
            """,
            (student_id,),  # parameters are always passed as a tuple
        ).fetchone()  # one dict, or None when no row matched

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.post("/students", status_code=201)
def create_student(name: str, course_id: int):
    """Task 4: create a student.
    name and course_id are plain function parameters, so FastAPI reads them
    from the query string (e.g. POST /students?name=Avery&course_id=1)."""
    try:
        with get_connection() as conn:
            # RETURNING hands back the new row (including the generated id)
            # in the same round trip, so we do not need a second SELECT.
            return conn.execute(
                f"""
                INSERT INTO {SCHEMA}.students (name, course_id)
                VALUES (%s, %s)
                RETURNING id, name, course_id
                """,
                (name, course_id),
            ).fetchone()
    except psycopg.errors.ForeignKeyViolation:
        # The database rejected a course_id that is not in courses
        raise HTTPException(status_code=400, detail="course_id does not exist")


@app.put("/students/{student_id}")
def update_student(student_id: int, name: str, course_id: int):
    """Task 4: replace a student's name and course. 404 if the id does not exist."""
    try:
        with get_connection() as conn:
            student = conn.execute(
                f"""
                UPDATE {SCHEMA}.students
                SET name = %s, course_id = %s
                WHERE id = %s
                RETURNING id, name, course_id
                """,
                (name, course_id, student_id),
            ).fetchone()
    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="course_id does not exist")

    # If no row matched the WHERE, RETURNING gives nothing and fetchone() is None
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    """Task 5: delete a student and return the deleted row. 404 if not found."""
    with get_connection() as conn:
        student = conn.execute(
            f"""
            DELETE FROM {SCHEMA}.students
            WHERE id = %s
            RETURNING id, name, course_id
            """,
            (student_id,),
        ).fetchone()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
