def test_api_get_story_list(mocker, mock_dynamo_driver, application_client, test_data):
    mocker.patch(
        "api.story.data_source.get_story_list",
        return_value=mock_dynamo_driver.get_story_list(),
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


def test_api_get_story_node(mocker, mock_dynamo_driver, application_client, test_data):
    story_id, node_id = "test_id", "Root"
    mocker.patch(
        "api.story.data_source.get_node",
        return_value=mock_dynamo_driver.get_node(story_id, node_id),
    )
    data = application_client.get(f"api/story/{story_id}/nodes/{node_id}")
    assert data.status_code == 200
    assert data.get_json() == {
        "options": [
            {"next": "Branch1-test1", "text": "br1"},
            {"next": "Branch2-test1", "text": "br2"},
        ],
        "text": "root",
    }


def test_api_get_not_exist_story_node(
    mocker, mock_dynamo_driver, application_client, test_data
):
    story_id, node_id = "test_id", "not_exist"
    mocker.patch(
        "api.story.data_source.get_node",
        return_value=mock_dynamo_driver.get_node(story_id, node_id),
    )
    data = application_client.get(f"api/story/{story_id}/nodes/{node_id}")
    assert data.status_code == 404


def test_api_get_story(mocker, mock_dynamo_driver, application_client, test_data):
    story_id = "test_id"
    mocker.patch(
        "api.story.data_source.get_story",
        return_value=mock_dynamo_driver.get_story(story_id),
    )
    data = application_client.get(f"api/story/{story_id}")
    assert data.status_code == 200
    assert data.get_json() == {
        "id": "test_id",
        "root": "Root",
        "name": "test_story",
    }


def test_api_get_not_exist_story(
    mocker, mock_dynamo_driver, application_client, test_data
):
    story_id = "not_found"
    mocker.patch(
        "api.story.data_source.get_story",
        return_value=mock_dynamo_driver.get_story(story_id),
    )
    data = application_client.get(f"api/story/{story_id}")
    assert data.status_code == 404
