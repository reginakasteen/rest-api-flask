def test_valid_registration(test_client, init_db):
    response = test_client.post(
        "/users/",
        json={
            "username": "test_user",
            "password": "password"
        }
    )

    assert response.status_code == 201
    assert "id" in response.json
    assert "username" in response.json
    assert "password" not in response.json
    

def test_invalid_registration(test_client, init_db):
    response = test_client.post(
        "/users/",
        json={
            "username": "test_user",
            "password": "123"
        }
    )
    assert response.status_code == 422
    assert response.json["password"] == ["Shorter than minimum length 5."]
    assert "password" in response.json


def test_double_registration(test_client, init_db):
    response = test_client.post(
        "/users/",
        json={
            "username": "test_user",
            "password": "password"
        }
    )

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "User already exist"
    

def test_valid_login(test_client, init_db):
    response = test_client.post(
        "/users/login",
        json={
            "username": "fiona",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json
    

def test_invalid_login(test_client, init_db):
    response = test_client.post(
        "/users/login",
        json={
            "username": "fiona",
            "password": "123password"
        }
    )

    assert response.status_code == 401
    assert "access_token" not in response.json
    assert response.json["error"] == "Wrong username or password"