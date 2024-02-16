from sqlite3 import IntegrityError
from ..main import app
from ..database import Base
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm.session import sessionmaker
from ..routers.todos import get_db,get_current_user
import pytest
from ..models import Todos



SQLALCHEMY_DATABASE_URL = "sqlite:///testdb.db"

# https://stackoverflow.com/a/39024742/13842101
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
    )


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)



def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()



def orreride_get_current_uer():
    return {
        "username":'harish',
        'user_id':1,
        "user_role":'admin'
    }

# app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = orreride_get_current_uer

# client = TestClient(app)

@pytest.fixture
def db():
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    _db = TestingSessionLocal()

    try:
        yield _db
    except IntegrityError:
        _db.rollback()  # Roll back the transaction in case of an IntegrityError
    finally:
        _db.close()  # Close the session

    with engine.connect() as connection:
        # Drop all data after each test
        for tbl in reversed(Base.metadata.sorted_tables):
            connection.execute(tbl.delete())

    # Put back the connection to the connection pool
    engine.dispose()


# pytest fixtures helps us reuse python objects like class
@pytest.fixture
def test_todos(db):
    todo = Todos(
        title = 'Learn to skip!!',
        description = 'SOEM DESCRIPTION FOR YOU',
        priority = 1,
        complete = False,
        owner_id =1)
    
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        for tbl in reversed(Base.metadata.sorted_tables):
            connection.execute(tbl.delete())
            connection.commit()