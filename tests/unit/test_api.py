from fastapi.testclient import TestClient

from services.api.app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_command_review_flow():
    response = client.post("/api/commands", json={"text": "/sync review PR #42"})
    assert response.status_code == 200
    body = response.json()
    assert body["parsed"]["agent"] == "reviewer"
    assert body["result"]["kind"] == "review"
    assert body["result"]["overallScore"] >= 80
    assert body["result"]["context"]["mcp"][0]["source"] == "github"
    assert body["result"]["context"]["rts"][0]["channel"] == "#dev-agent-ops"


def test_slack_form_command_flow():
    response = client.post(
        "/slack/commands",
        data={"text": "review PR #42"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["response_type"] == "ephemeral"
    assert "merge-ready" in body["text"]
