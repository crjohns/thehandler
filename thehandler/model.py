import thehandler
import json
import random
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
Base = declarative_base()

names = None

engine = None

def loadNames():
    global names
    f = open('data/names.json').read()
    names = json.loads(f)

def saveNames(session):
    if not names:
        loadNames()

    addus = []

    for entry in names:
        addus.append( Name( name = entry['name'], \
                            gender = entry['gender'], \
                            part = entry['part'], \
                            nation = entry['nation']))

    session.add_all(addus)
    session.commit()



def getName(gender):
    if not names:
        loadNames()

    firsts = filter(lambda x: x['gender'] == gender and x['part'] == 'first', names)
    anylast = filter(lambda x: x['part'] == 'last' and (x['gender'] in ['any',gender]), names)

    first = random.sample(firsts,1)[0]['name'].capitalize()
    last = random.sample(anylast,1)[0]['name'].capitalize()

    return (str(first), str(last))


class Name(Base):
    __tablename__ = 'randnames'
    id = Column(Integer, primary_key = True)
    name = Column(String, index = True)
    gender = Column(String, index = True)
    part = Column(String, index = True)
    nation = Column(String, index = True)

    def __init__(self, name, gender, part, nation):
        self.name = name
        self.gender = gender
        self.part = part
        self.nation = nation

    def __repr__(self):
        return "(Name '%s', %s, %s, %s)" % (self.name, self.gender, self.part, self.nation)

class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    abbrev = Column(String)
    agencies = relationship('Agency')

    def __init__(self, name, abbrev):
        self.name = name
        self.abbrev = abbrev

class Agency(Base):
    __tablename__ = 'agency'
    id = Column(Integer, primary_key = True)
    fullname = Column(String)
    nickname = Column(String)
    country = Column(Integer, ForeignKey('country.id'))

    def __init__(self, fullname, nickname):
        self.fullname = fullname
        self.nickname = nickname


def openDB(gamename, newgame=False, debug=False):
    global engine 
    global Base

    dbname = 'sqlite:///%s.db' % gamename
    engine = create_engine(dbname, echo=debug)

    if newgame:
        Base.metadata.create_all(engine)

    Session = sessionmaker(bind = engine)
    
    return Session()



