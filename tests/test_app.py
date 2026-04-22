"""
FastAPI tests for Mergington High School API using AAA (Arrange-Act-Assert) pattern.
Tests cover all three endpoints: GET /, GET /activities, and POST /activities/{activity_name}/signup
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


class TestGetRoot:
    """Tests for the root endpoint (GET /)"""

    def test_get_root_redirect(self, client):
        """
        Test that GET / redirects to /static/index.html
        
        Arrange: TestClient is ready via fixture
        Act: Make GET request to /
        Assert: Verify 307 redirect status and correct location header
        """
        # Arrange
        expected_redirect_url = "/static/index.html"
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == expected_redirect_url


class TestGetActivities:
    """Tests for the activities list endpoint (GET /activities)"""

    def test_get_activities_returns_all(self, client):
        """
        Test that GET /activities returns all activities with expected structure
        
        Arrange: Set up expected activity names and keys
        Act: Make GET request to /activities
        Assert: Verify all activities are returned with correct structure
        """
        # Arrange
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Soccer Club", "Art Club", "Music Band", "Debate Club", "Science Club"
        ]
        expected_keys = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert set(activities_data.keys()) == set(expected_activities)
        
        # Verify each activity has required structure
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_info, dict)
            assert set(activity_info.keys()) == expected_keys
            assert isinstance(activity_info["participants"], list)


class TestSignupForActivity:
    """Tests for the signup endpoint (POST /activities/{activity_name}/signup)"""

    def test_signup_for_activity_success(self, client, sample_emails):
        """
        Test successful signup for an activity with a new participant
        
        Arrange: Select an activity and a new email not currently signed up
        Act: Make POST request to signup endpoint with email query parameter
        Assert: Verify success message is returned and response shows correct data
        """
        # Arrange
        activity_name = "Programming Class"
        new_email = sample_emails["new"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        response_data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert response_data["message"] == f"Signed up {new_email} for {activity_name}"

    def test_signup_for_activity_new_participant(self, client, sample_emails):
        """
        Test that a new participant is added to the activity's participant list
        
        Arrange: Get the current activity, select a new email, record initial count
        Act: Make signup request with new email, then fetch activities to verify
        Assert: Verify the email was added to the activity's participants list
        """
        # Arrange
        activity_name = "Art Club"
        new_email = sample_emails["another_new"]
        
        # Get activities to check initial state
        activities_before = client.get("/activities").json()
        initial_participants = activities_before[activity_name]["participants"].copy()
        
        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Fetch activities again to see updated state
        activities_after = client.get("/activities").json()
        updated_participants = activities_after[activity_name]["participants"]
        
        # Assert
        assert signup_response.status_code == 200
        assert new_email not in initial_participants
        assert new_email in updated_participants
        assert len(updated_participants) == len(initial_participants) + 1
