def test_api_get_story_list(
    mocker, mock_dynamodb_driver, application_client, test_data
):
    mocker.patch(
        "api.story.data_source.get_story_list",
        return_value=mock_dynamodb_driver.get_story_list(),
    )
    data = application_client.get("api/story")
    assert data.status_code == 200
    assert data.get_json() == {
        "stories": [
            {
                key: value
                for key, value in test_data.items()
                if key in ("id", "root", "name")
            }
        ]
    }


def test_api_get_story_node(
    mocker, mock_dynamodb_driver, application_client, test_data
):
    story_id, node_id = "1", "Root"
    mocker.patch(
        "api.story.data_source.get_node",
        return_value=mock_dynamodb_driver.get_node(story_id, node_id),
    )
    data = application_client.get(f"api/story/{story_id}/nodes/{node_id}")
    assert data.status_code == 200
    assert data.get_json() == {
        "options": [
            {"next": None, "text": "br2"},
            {"next": "Root1", "text": "br1"},
        ],
        "text": "root",
    }


def test_api_get_not_exist_story_node(
    mocker, mock_dynamodb_driver, application_client, test_data
):
    story_id, node_id = "1", "not_exist"
    mocker.patch(
        "api.story.data_source.get_node",
        return_value=mock_dynamodb_driver.get_node(story_id, node_id),
    )
    data = application_client.get(f"api/story/{story_id}/nodes/{node_id}")
    assert data.status_code == 404


def test_api_get_story(mocker, mock_dynamodb_driver, application_client, test_data):
    story_id = "1"
    mocker.patch(
        "api.story.data_source.get_story",
        return_value=mock_dynamodb_driver.get_story(story_id),
    )
    data = application_client.get(f"api/story/{story_id}")
    assert data.status_code == 200
    assert data.get_json() == {
        "id": "1",
        "root": "Root",
        "name": "test_story",
    }


def test_api_get_not_exist_story(
    mocker, mock_dynamodb_driver, application_client, test_data
):
    story_id = "not_found"
    mocker.patch(
        "api.story.data_source.get_story",
        return_value=mock_dynamodb_driver.get_story(story_id),
    )
    data = application_client.get(f"api/story/{story_id}")
    assert data.status_code == 404
