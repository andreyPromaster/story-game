import logging
from functools import wraps

from sqlalchemy.exc import DataError, NoResultFound
from sqlalchemy.orm import sessionmaker

from common.entities import schemas
from data_storage.data_source import DataDriver
from data_storage.sqlalchemy.models import (
    Node,
    Option,
    Story,
    StoryRoot,
    get_connection_engine,
)

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def execute_query(method):
    @wraps(method)
    def inner(self, *args, **kwargs):
        with self.session.begin():
            return method(self, *args, **kwargs)

    return inner


def handle_exception(method):
    @wraps(method)
    def inner(self, *args, **kwargs):
        try:
            data = method(self, *args, **kwargs)
            return data
        except (NoResultFound, DataError):
            return None

    return inner


class RDSDriver(DataDriver):
    def __init__(self, session=None):
        if session is None:
            engine = get_connection_engine()
            Sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            self.session = Sessionmaker()
        else:
            self.session = session

    @handle_exception
    @execute_query
    def get_story(self, story_id: str):
        story = (
            self.session.query(Story)
            .filter(
                Story.id == story_id,
            )
            .one()
        )
        root_node = (
            self.session.query(StoryRoot.node)
            .filter(StoryRoot.story == story_id)
            .scalar_subquery()
        )
        node = self.session.query(Node.name).filter(Node.id == root_node).one()
        return schemas.Story(id=story.id, root=node.name, name=story.name)

    @handle_exception
    @execute_query
    def get_node(self, story_id: str, uri: str):
        node = (
            self.session.query(Node)
            .filter(
                Node.story == story_id,
                Node.name == uri,
            )
            .one()
        )
        options = (
            self.session.query(Option.text, Node.name.label("next"))
            .join(Node, Option.next == Node.id, isouter=True)
            .filter(
                Option.cur_node == node.id,
            )
            .order_by(Option.id)
            .all()
        )
        return schemas.Node(text=node.text, options=options)

    @handle_exception
    @execute_query
    def get_story_list(self):
        stories = (
            self.session.query(Story.id, Story.name, Node.name.label("root"))
            .join(StoryRoot, Story.id == StoryRoot.story, isouter=True)
            .join(Node, StoryRoot.node == Node.id, isouter=True)
            .all()
        )
        return schemas.StoryList(stories=stories)

    @execute_query
    def _create_story(self, data: schemas.StoryItem):
        story = Story(id=data.id, name=data.name)
        self.session.add(story)
        self.session.flush()

        nodes = {
            node_name: Node(story=story.id, name=node_name, text=node_data.text)
            for node_name, node_data in data.nodes.items()
        }
        self.session.add_all(list(nodes.values()))
        self.session.flush()

        root_node = nodes[data.root]
        story_root = StoryRoot(story=story.id, node=root_node.id)
        self.session.add(story_root)
        self.session.flush()

        options = []
        for node_name, node_data in data.nodes.items():
            for option in node_data.options:
                cur_node = nodes[node_name]
                next_node = nodes.get(option.next)
                new_option = Option(
                    cur_node=cur_node.id,
                    text=option.text,
                    next=next_node.id if next_node else None,
                )
                options.append(new_option)
        self.session.add_all(options)
        self.session.flush()
