from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from blog import recreate_tables, User

from pytest import fixture

@fixture
def session():
    engine = create_engine('postgresql+pg8000://postgres:secret@localhost:5432/postgres')
    recreate_tables(engine)
    session = Session(bind=engine)
    yield session
    session.close()


class TestBlog:
    def test_user(self, session):
        session.add(User(username='john', email='john@example.com'))
        session.commit()
        finded_user = session.query(User).first()
        assert finded_user.username == 'john'
        assert finded_user.email == 'john@example.com'