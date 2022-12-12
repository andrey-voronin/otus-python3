from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    enabled = Column(Boolean, default=True)
    created_on = Column(DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f'User(user_id={self.user_id!r}, username={self.username!r}, email={self.email!r}, enabled={self.enabled}, created_on={self.created_on!r})'


class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.user_id'))
    title = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.now)
    updated_on = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'Post(post_id={self.post_id!r}, user_id={self.user_id!r}, title={self.title!r}, content={self.content!r}, created_on={self.created_on!r}, updated_on={self.updated_on!r})'


class Comment(Base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.user_id'))
    post_id = Column(ForeignKey('posts.post_id'))
    content = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.now)
    updated_on = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'Comment(comment_id={self.comment_id!r}, user_id={self.user_id!r}, post_id={self.post_id!r}, content={self.content!r}, created_on={self.created_on!r}, updated_on={self.updated_on!r})'


class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    price = Column(Numeric(5, 2), nullable=False)

    def __repr__(self):
        return f'Product(product_id={self.product_id!r}, name={self.name!r}, description={self.description!r}, price={self.price})'


def recreate_tables(engine):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def insert_test_data(engine):
    session = Session(bind=engine)
    blogger = User(username='blogger', email='blogger@example.com')
    commenter = User(username='commenter', email='commenter@example.com')
    session.add(blogger)
    session.add(commenter)
    session.commit()
    test_post = Post(user_id=blogger.user_id, title='Welcome to blog', content='I am glad to see you are interested in my pages')
    session.add(test_post)
    session.commit()
    test_comment = Comment(user_id=commenter.user_id, post_id=test_post.post_id, content='Your blog needs greate improvements')
    session.add(test_comment)
    session.add(Product(name='Weather station', description='Portable weather station', price=295.94))
    session.commit()
    session.close()


if __name__ == '__main__':
    engine = create_engine('postgresql+pg8000://postgres:secret@localhost:5432/postgres', echo=True)
    recreate_tables(engine)
    insert_test_data(engine)
