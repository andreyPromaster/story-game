import logging
from functools import wraps

from sqlalchemy.exc import DataError, NoResultFound
from sqlalchemy.orm import sessionmaker

from common.entities import schemas
from data_storage.data_source import DataDriver
from data_storage.sqlalchemy.models import Node, Option, Story, get_connection_engine

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
            self.session.query(Story.id, Story.name, Node.name.label("root"))
            .join(Node, isouter=True)
            .filter(
                Story.id == story_id,
                Node.name == "Root",
            )
            .one()
        )
        return schemas.Story.from_orm(story)

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
            .join(Node, isouter=True)
            .filter(Node.name == "Root")
            .all()
        )
        return schemas.StoryList(stories=stories)

    @execute_query
    def _create_story(self, data: schemas.StoryItem):
        savepoint = self.session.begin_nested()
        story = Story(id=data.id, name=data.name)
        self.session.add(story)
        savepoint.commit()

        savepoint = self.session.begin_nested()
        nodes = [
            Node(
                story=story.id,
                name=node_name,
                text=node_data.text,
                is_root=node_name == data.root,
            )
            for node_name, node_data in data.nodes.items()
        ]
        self.session.add_all(nodes)
        savepoint.commit()

        savepoint = self.session.begin_nested()
        options = []
        for node_name, node_data in data.nodes.items():
            for option in node_data.options:
                cur_node = list(filter(lambda node: node.name == node_name, nodes))[0]
                next_node = list(filter(lambda node: node.name == option.next, nodes))
                new_option = Option(
                    cur_node=cur_node.id,
                    text=option.text,
                    next=next_node[0].id if next_node else None,
                )
                options.append(new_option)
        self.session.add_all(options)
        savepoint.commit()
