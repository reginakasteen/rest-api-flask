def test_no_expenses_list(test_client, init_db, second_user_token):
    response = test_client.get(
        "/expenses/",
        headers={
            "Authorization": f"Bearer {second_user_token}"
        }
    )

    assert response.status_code == 200
    assert response.json == []

def test_expenses_list(test_client, init_db, default_user_token):
    response = test_client.get(
        "/expenses/",
        headers={
            "Authorization": f"Bearer {default_user_token}"
        }
    )

    assert response.status_code == 200
    assert len(response.json) > 0

    