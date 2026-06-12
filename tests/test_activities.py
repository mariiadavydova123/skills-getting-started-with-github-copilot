"""
Tests for the GET /activities endpoint.
Uses AAA (Arrange-Act-Assert) pattern.
"""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities in the system."""
    # Arrange
    # Activities are already populated in the fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities_data = response.json()
    assert isinstance(activities_data, dict)
    assert len(activities_data) > 0
    assert "Chess Club" in activities_data
    assert "Programming Class" in activities_data


def test_get_activities_includes_required_fields(client):
    """Test that each activity has all required fields."""
    # Arrange
    # Activities are already populated in the fixture

    # Act
    response = client.get("/activities")
    activities_data = response.json()

    # Assert
    for activity_name, activity_details in activities_data.items():
        assert "description" in activity_details
        assert "schedule" in activity_details
        assert "max_participants" in activity_details
        assert "participants" in activity_details
        assert isinstance(activity_details["participants"], list)


def test_get_activities_participants_are_email_strings(client):
    """Test that participants are stored as email strings."""
    # Arrange
    # Activities are already populated in the fixture

    # Act
    response = client.get("/activities")
    activities_data = response.json()

    # Assert
    for activity_name, activity_details in activities_data.items():
        for participant in activity_details["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email check
