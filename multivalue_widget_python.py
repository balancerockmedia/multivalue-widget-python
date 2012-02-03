from flask import Flask
from flask import render_template, abort, redirect, url_for, request
from flaskext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:@127.0.0.1:3306/multivalue_widget'

db = SQLAlchemy(app)

user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), nullable=False)
)

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

"""
from multivalue_widget_python import db
db.create_all()
"""

def build_tree(skill_id, name):
    num_children = Skill.query.filter_by(parent=Skill.query.get(skill_id)).count()
    
    retval = ''
    
    if (num_children > 0):
        retval += '<li><div><span rel="'+str(skill_id)+'">'+name+'</span><span><a href="#" class="open">open</a></span></div>'
        
        retval += '<ul>'
        
        skills = Skill.query.filter_by(parent=Skill.query.get(skill_id))
        
        for skill in skills:
            retval += build_tree(skill.id, skill.name);
                                
        retval += '</ul></li>'
    else:
        retval += '<li><div><span rel="'+str(skill_id)+'">'+name+'</span><span><a href="#" class="add">add</a></span></div></li>'
        
    return retval

@app.route('/')
def index():
    user = User.query.get(1)
    
    # left side skills
    root_level_skills = Skill.query.filter_by(parent=None).all()
    
    left_side_skills = '<ul>'
    
    if (len(root_level_skills) > 0):
        for skill in root_level_skills:                            
            left_side_skills += build_tree(skill.id, skill.name)
                            
    left_side_skills += '</ul>';
    
    # right side skills
    right_side_skills = ''
    
    if (len(user.skills) < 1):
        right_side_skills += '<li style="margin: 0 0 10px">No Skills Selected</li>'
    else:
        for skill in user.skills:
             right_side_skills += '<li><div><span>'+skill.name+'</span><span><a href="#" class="remove">remove</a><input type="hidden" name="skill" value="'+str(skill.id)+'" /></span></div></li>';
    
    return render_template('home.html', user=user, left_side_skills=left_side_skills, right_side_skills=right_side_skills)
    
@app.route('/user/<id>', methods=['POST'])
def update_user(id):
    skills = request.form.getlist('skill')
    
    user = User.query.get(id)
    user.firstname = request.form['firstname']
    user.lastname = request.form['lastname']
    
    # delete all skills for this user
    # TODO can't figure out how to do this using the ORM
    # del user.skills[:]
    db.session.execute('DELETE FROM user_skills WHERE user_id = '+str(user.id))
    db.session.flush()
    
    # add new skills
    for skill in skills:
        user.skills.append(Skill.query.get(skill))
    
    db.session.commit()
    
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.debug = True
    app.run()
