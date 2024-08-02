import pytest
from sqlmodel import SQLModel, Field, Session
from neut.db.base import engine, get_session, create_db_and_tables

class TestModel(SQLModel, table=True):
    # Simple Pytest hack
    __test__ = False

    id: int = Field(primary_key=True)
    name: str

@pytest.fixture(scope="module")
def setup_test_db():
    create_db_and_tables()
    yield
    SQLModel.metadata.drop_all(engine)

def test_create_and_read(setup_test_db):
    with Session(engine) as session:
        test_model = TestModel(name="Test")
        session.add(test_model)
        session.commit()
        session.refresh(test_model)
        
        retrieved = session.get(TestModel, test_model.id)
        assert retrieved.name == "Test"

def test_get_session():
    session = next(get_session())
    assert isinstance(session, Session)