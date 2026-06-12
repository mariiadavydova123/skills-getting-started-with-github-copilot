import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


@pytest.fixture
def client():
    """Create a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """
    Provide a fresh copy of activities for each test
    to ensure test isolation
    """
    return copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities(fresh_activities):
    """
    Auto-reset the activities database to fresh state before each test
    """
    activities.clear()
    activities.update(fresh_activities)
    yield
    activities.clear()
    activities.update(fresh_activities)
