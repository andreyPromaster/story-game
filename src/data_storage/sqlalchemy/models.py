from sqlalchemy import NVARCHAR, Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base

# if NOT_A_LAZY_CONNECTION:
#     engine = get_connection(tunnelled=USE_RDS_PROXY)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# else:
#     engine = LazyConnection(tunnelled=USE_RDS_PROXY)
#     SessionLocal = None

Base = declarative_base(bind=engine)


class Story(Base):
    __tablename__ = "story"
    root = Column(
        Integer, ForeignKey("node.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name = Column(NVARCHAR(200), nullable=False)


class Node(Base):
    __tablename__ = "node"
    story = Column(
        Integer, ForeignKey("story.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name = Column(NVARCHAR(200), nullable=False)
    text = Column(NVARCHAR(200), nullable=False)


class Option(Base):
    __tablename__ = "option"
    next = Column(
        Integer, ForeignKey("node.id", ondelete="CASCADE"), nullable=False, index=True
    )
    text = Column(NVARCHAR(200), nullable=False)
