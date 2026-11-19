"""Shared test setup.

These tests call the REAL Supabase database (fastapi_practice schema).
Before and after every test, sql/reset.sql puts the data back to the seed state,
so tests cannot affect each other.
"""
import importlib
import os
from pathlib import Path

import psycopg
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

RESET_SQL = (ROOT / "sql" / "reset.sql").read_text()


@pytest.fixture(scope="session", autouse=True)
def check_env():
    """Stop early with a clear message if .env has not been filled in."""
    url = os.getenv("DATABASE_URL", "")
    if not url or "YOUR_DB_PASSWORD" in url:
        pytest.exit("Put your real database password in .env (DATABASE_URL) first.", returncode=2)


@pytest.fixture(autouse=True)
def reset_database():
    """Runs around every test: reset, run the test, reset again."""
    url = os.environ["DATABASE_URL"].replace("postgresql+psycopg://", "postgresql://", 1)
    # reset.sql has several statements and no parameters, which psycopg allows in one execute()
    with psycopg.connect(url) as conn:
        conn.execute(RESET_SQL)
    yield
    with psycopg.connect(url) as conn:
        conn.execute(RESET_SQL)


@pytest.fixture(params=["v1_psycopg", "v2_orm"])
def api(request):
    """Run each test twice: once against v1, once against v2.
    Returns (version_name, client). TestClient calls the app in-process, so there is
    no need to start a server."""
    module = importlib.import_module(f"{request.param}.main")
    with TestClient(module.app) as client:
        yield request.param, client


def send_student(api, method, path, name, course_id):
    """The two versions take input differently:
    v1 uses query parameters (?name=..&course_id=..), v2 uses a JSON body.
    This helper hides that difference so one test can cover both."""
    version, client = api
    data = {"name": name, "course_id": course_id}
    if version == "v1_psycopg":
        return client.request(method, path, params=data)
    return client.request(method, path, json=data)
