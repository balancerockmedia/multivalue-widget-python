from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
Base = declarative_base()

""" Create join table for users and skills """
user_skills = Table('user_skills', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('skill_id', Integer, ForeignKey('skills.id'), nullable=False)
)

""" User model """
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    
    skills = relationship('Skill', secondary=user_skills, single_parent=True)
    
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return '<User %r>' % self.firstname

""" Skill model """ 
class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey('skills.id'))
    
    parent = relationship('Skill', remote_side=[id])
    
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def __repr__(self):
        return '<User %r>' % self.name
        
def create_tables(engine):
    Base.metadata.create_all(engine)
    
def drop_tables(engine):
    Base.metadata.drop_all(engine, checkfirst=False)