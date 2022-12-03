import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from allocation.infrastructure.models import Base


@pytest.fixture(scope="session")
def in_memory_db():
    engine = create_engine("sqlite:///:memory:", echo=True, future=True)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    with Session(in_memory_db) as session:
        yield session
        session.rollback()
