import pytest


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/users",
        json={"email": "alice@example.com", "full_name": "Alice Smith"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["email"] == "alice@example.com"
    assert payload["full_name"] == "Alice Smith"
    assert "id" in payload


@pytest.mark.asyncio
async def test_create_user_rejects_duplicate_email(client):
    payload = {"email": "alice@example.com", "full_name": "Alice Smith"}

    first_response = await client.post("/users", json=payload)
    second_response = await client.post("/users", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert "already exists" in second_response.json()["detail"]


@pytest.mark.asyncio
async def test_get_user_returns_404_when_missing(client):
    response = await client.get("/users/00000000-0000-0000-0000-000000000001")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_users_supports_pagination(client):
    for index in range(3):
        response = await client.post(
            "/users",
            json={"email": f"user{index}@example.com", "full_name": f"User {index}"},
        )
        assert response.status_code == 201

    response = await client.get("/users", params={"limit": 2, "offset": 1})

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 3
    assert payload["limit"] == 2
    assert payload["offset"] == 1
    assert len(payload["items"]) == 2


@pytest.mark.asyncio
async def test_delete_user_removes_owned_projects(client):
    user_response = await client.post(
        "/users",
        json={"email": "owner@example.com", "full_name": "Owner"},
    )
    user_id = user_response.json()["id"]

    project_response = await client.post(
        "/projects",
        json={"name": "Modernization", "description": "POC", "owner_id": user_id},
    )
    project_id = project_response.json()["id"]

    delete_response = await client.delete(f"/users/{user_id}")
    project_fetch_response = await client.get(f"/projects/{project_id}")

    assert delete_response.status_code == 204
    assert project_fetch_response.status_code == 404
