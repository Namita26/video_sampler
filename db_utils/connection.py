from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, Table

engine = create_engine('mysql+mysqldb://root:root@localhost/glamrscms', echo=True)

Base = declarative_base()
metadata = MetaData()

'''

class Categories(Base):
    __tablename__ = 'Categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(1000))

    def repr(self):
        return "<Category(name=%s)" % (self.name)
'''
Categories = Table(
    'Categories', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(1000)),
)

metadata.create_all(engine)


