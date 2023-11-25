from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///alchemy.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class UserTable(Base):
    __tablename__ = 'user_table'
    user_id = Column(Integer, primary_key=True)
    user_telegram_id = Column(String(20), unique=True)
    username = Column(String)
    created = Column(String)
    message = relationship('UserMessages')


class UserMessages(Base):
    __tablename__ = 'user_message'
    message_id = Column(Integer, primary_key=True)
    text = Column(String)
    created = Column(String)
    user_id = Column(Integer, ForeignKey("user_table.user_id"))
    user = relationship('UserTable')






Base.metadata.create_all(engine)
