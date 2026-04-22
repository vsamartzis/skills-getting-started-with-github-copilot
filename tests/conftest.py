"""
Pytest configuration and fixtures for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for making requests to the app.
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Fixture that provides a fresh copy of the activities dictionary for each test.
    This ensures test isolation - modifications in one test don't affect others.
    """
    return copy.deepcopy(activities)


@pytest.fixture
def sample_emails():
    """
    Fixture that provides sample email addresses for testing signup functionality.
    """
    return {
        "existing": "michael@mergington.edu",  # Already signed up for Chess Club
        "new": "newstudent@mergington.edu",     # Not signed up for any activity
        "another_new": "anotherstudent@mergington.edu"  # Another new email
    }
