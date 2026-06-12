"""
Tests for the POST /activities/{activity_name}/signup endpoint.
Uses AAA (Arrange-Act-Assert) pattern.
"""


def test_signup_for_activity_success(client):
    """Test that a new student can successfully sign up for an activity."""
    # Arrange
    email = "test.student@mergington.edu"
    activity_name = "Chess Club"
    initial_activities = client.get("/activities").json()
    initial_count = len(initial_activities[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    
    updated_activities = client.get("/activities").json()
    assert email in updated_activities[activity_name]["participants"]
    assert len(updated_activities[activity_name]["participants"]) == initial_count + 1


def test_signup_returns_success_message(client):
    """Test that signup endpoint returns the correct success message."""
    # Arrange
    email = "alice@mergington.edu"
    activity_name = "Programming Class"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for {activity_name}"


def test_signup_adds_participant_to_correct_activity(client):
    """Test that signup adds the participant to the correct activity."""
    # Arrange
    email = "bob@mergington.edu"
    activity_name = "Swimming Club"
    other_activity = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    updated_activities = client.get("/activities").json()
    assert email in updated_activities[activity_name]["participants"]
    assert email not in updated_activities[other_activity]["participants"]
