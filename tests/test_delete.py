"""
Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint.
Uses AAA (Arrange-Act-Assert) pattern.
"""


def test_delete_participant_success(client):
    """Test that a participant can be successfully removed from an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Known participant
    initial_activities = client.get("/activities").json()
    initial_count = len(initial_activities[activity_name]["participants"])

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    
    updated_activities = client.get("/activities").json()
    assert email not in updated_activities[activity_name]["participants"]
    assert len(updated_activities[activity_name]["participants"]) == initial_count - 1


def test_delete_returns_success_message(client):
    """Test that delete endpoint returns the correct success message."""
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Known participant

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Removed {email} from {activity_name}"


def test_delete_only_removes_target_participant(client):
    """Test that deleting a participant only removes that participant."""
    # Arrange
    activity_name = "Art Club"
    email_to_remove = "isabella@mergington.edu"
    other_email = "liam@mergington.edu"
    initial_activities = client.get("/activities").json()
    initial_participants = initial_activities[activity_name]["participants"].copy()

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email_to_remove}"
    )

    # Assert
    assert response.status_code == 200
    updated_activities = client.get("/activities").json()
    updated_participants = updated_activities[activity_name]["participants"]
    
    assert email_to_remove not in updated_participants
    assert other_email in updated_participants
    assert len(updated_participants) == len(initial_participants) - 1
