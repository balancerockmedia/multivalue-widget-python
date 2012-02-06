import os
import unittest
from flaskext.sqlalchemy import SQLAlchemy
import multivalue_widget_python as mvp
from models import db
from models import User
from models import Skill

class AppTestCase(unittest.TestCase):
    
    def setUp(self):
        # self.app = mvp.app.test_client()
        
        self.app = mvp.create_app('./settings/test.cfg')
        
        # db.init_app(self.app)
        
        db.create_all()
        
    def tearDown(self):
        mvp.db.drop_all()
        
    def test_create_user(self):
        user = mvp.User('Dan', 'Johnson')
        mvp.db.session.add(user)
        mvp.db.session.commit()
        
        self.assertEqual(user.id, 1)
        
    def test_create_skill(self):
        skill = mvp.Skill('Dan', 'Johnson')
        mvp.db.session.add(skill)
        mvp.db.session.commit()
        
        self.assertEqual(skill.id, 1)
        
if __name__ == '__main__':
    unittest.main()