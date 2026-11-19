"""Task 1 only exists in v1 (GET /database), so it has its own test."""
from fastapi.testclient import TestClient

from v1_psycopg.main import app


def test_database_endpoint_returns_database_name():
    with TestClient(app) as client:
        response = client.get("/database")
    assert response.status_code == 200
    assert response.json()["database"] == "postgres"  # Supabase's default database name
