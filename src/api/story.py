from flask import Blueprint, abort, jsonify, request

from data_storage.connection import get_data_source
from utilities.exceptions import ValidationError

story_api = Blueprint("story_api_br", __name__)
data_source = get_data_source()


@story_api.route("/stories/<string:story_id>", methods=["GET"])
def get_story(story_id):
    story = data_source.get_story(story_id=story_id)
    if story is not None:
        return jsonify(story.dict())
    else:
        abort(404)


@story_api.route("/stories", methods=["GET", "POST"])
def create_or_get_list_story():
    if request.method == "POST":
        data = request.get_json()
        try:
            saved_data = data_source.create_story(data)
        except ValidationError as e:
            return jsonify(e.message), 400
        return jsonify(saved_data.dict()), 201
    if request.method == "GET":
        stories = data_source.get_story_list()
        return jsonify(stories.dict())


@story_api.route("/stories/<string:story_id>/nodes/<string:uri>", methods=["GET"])
def get_story_node(story_id, uri):
    node = data_source.get_node(story_id=story_id, uri=uri)
    if node is not None:
        return jsonify(node.dict())
    else:
        abort(404)
