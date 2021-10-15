from flask import Blueprint, abort, jsonify

from entities.data_source import get_data_source

story_api = Blueprint("story_api_br", __name__)
data_source = get_data_source()


@story_api.route("/story/<string:story_id>")
def get_story(story_id):
    story = data_source.get_story(story_id=story_id)
    if story is not None:
        return jsonify(story.dict())
    else:
        abort(404)


@story_api.route("/story")
def list_story():
    stories = data_source.get_story_list()
    return jsonify(stories)


@story_api.route("/story/<string:story_id>/nodes/<string:uri>")
def get_story_node(story_id, uri):
    node = data_source.get_node(story_id=story_id, uri=uri)
    if node is not None:
        return jsonify(node.dict())
    else:
        abort(404)
