from sqlalchemy import Column,String,create_engine,Integer,DateTime,PickleType,Boolean,Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
Base =declarative_base()
engine=create_engine('mysql+pymysql://voiceprint:123456@localhost:3306/voiceproject1?charset=utf8')
DBSession = sessionmaker(engine)
class Agreelogin(Base):
    __tablename__='agree_login'
    id = Column(Integer,primary_key=True,autoincrement=True)
    identifier=Column(String(20),nullable=False)
    time = Column(DateTime,default=datetime.datetime.now)
    success = Column(Boolean,nullable=False)

class Agreeuser(Base):
    __tablename__='agree_users'
    id = Column(Integer,primary_key=True ,autoincrement=True)
    identifier=Column(String(20),nullable=False)
    voiceprint = Column(PickleType,nullable=False)
    key1 = Column(PickleType, nullable=False)
    key2 = Column(PickleType, nullable=False)
    keyH = Column(PickleType, nullable=False)
