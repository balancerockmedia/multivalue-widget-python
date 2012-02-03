from flaskext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

""" Create join table for users and skills """
user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), nullable=False)
)

""" User model """
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    
    skills = db.relationship('Skill', secondary=user_skills, cascade="all, delete, delete-orphan", single_parent=True)
    
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return '<User %r>' % self.firstname

""" Skill model """ 
class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('skills.id'))
    
    parent = db.relationship('Skill', remote_side=[id])
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name