import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db
from app.main import app
from app.models import db as models


# CONFIGURATION & FIXTURES (The Testing Environment Setup)


@pytest.fixture
def client():
    """
    Pytest fixture that sets up an isolated test database, overrides the 
    FastAPI database dependency, spins up a TestClient, and tears down 
    everything cleanly after the test finishes.
    """
    # 1. SETUP: Configure isolated SQLite file location
    test_db_path = Path(__file__).with_name("test.db")
    test_engine = create_engine(
        f"sqlite:///{test_db_path}",
        connect_args={"check_same_thread": False}, # Required for multi-threaded FastAPI tests
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    # 2. INITIALIZE: Ensure a totally clean database state before running
    models.Base.metadata.drop_all(bind=test_engine)
    models.Base.metadata.create_all(bind=test_engine)

    # 3. INTERCEPT: Inline dependency override function
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Bind the test database context to our live app dependency router
    app.dependency_overrides[get_db] = override_get_db

    # 4. EXECUTE: Hand off the active context browser to the test case
    with TestClient(app) as test_client:
        yield test_client

    # 5. TEARDOWN: Wipe sandbox database state and clean up engine resources
    app.dependency_overrides.clear()
    models.Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


# ==============================================================================
# AUTOMATED TEST CASES
# ==============================================================================

def test_login_with_wrong_password(client):
    """
    Verifies that an existing user attempting to log in with an incorrect
    password payload is securely rejected with a 401 Unauthorized response.
    """
    # 1. Arrange: Register a fresh user into the clean sandbox database
    client.post(
        "/auth/register",
        json={
            "name": "Tester Guy",
            "email": "tester@example.com",
            "password": "correct-password",
        },
    )

    payload = {
        "email": "tester@example.com",
        "password": "definitely_the_wrong_password",
    }

    # 2. Act: Attempt to log into the application with invalid credentials
    response = client.post("/auth/login", json=payload)

    # 3. Assert: Verify the server enforces authentication rules perfectly
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}