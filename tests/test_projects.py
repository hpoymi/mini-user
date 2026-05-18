import pytest


@pytest.mark.asyncio
async def test_create_project_for_existing_user(client):
    user_response = await client.post(
        "/users",
        json={"email": "architect@example.com", "full_name": "Architect"},
    )
    user_id = user_response.json()["id"]

    response = await client.post(
        "/projects",
        json={
            "name": "Client Platform Upgrade",
            "description": "Modernization roadmap POC",
            "owner_id": user_id,
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["owner_id"] == user_id
    assert payload["name"] == "Client Platform Upgrade"


@pytest.mark.asyncio
async def test_list_projects_by_user(client):
    user_response = await client.post(
        "/users",
        json={"email": "manager@example.com", "full_name": "Manager"},
    )
    user_id = user_response.json()["id"]

    for project_name in ("Alpha", "Beta"):
        response = await client.post(
            "/projects",
            json={"name": project_name, "description": None, "owner_id": user_id},
        )
        assert response.status_code == 201

    response = await client.get(f"/users/{user_id}/projects")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert {project["name"] for project in payload} == {"Alpha", "Beta"}
