from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_and_unregister_participant():
    activity_name = "Chess Club"
    email = "student.test@example.com"

    # ensure a clean state
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    if response.status_code == 200:
        pass

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    activity_response = client.get("/activities")
    activity_data = activity_response.json()
    assert email in activity_data[activity_name]["participants"]

    unregister_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Removed {email} from {activity_name}"

    updated_activity = client.get("/activities").json()
    assert email not in updated_activity[activity_name]["participants"]
