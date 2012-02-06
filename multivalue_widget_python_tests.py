import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import multivalue_widget_python as mvp
import models
from models import User
from models import Skill

class AppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = mvp.create_app('./settings/test.cfg')
        
        models.create_tables(self.app.engine)
        
        Session = sessionmaker(bind=self.app.engine)
        
        self.db = Session()
        
    def tearDown(self):
        self.db.close()
        models.drop_tables(self.app.engine)
        
    def test_create_user(self):
        user = User('Dan', 'Johnson')
        self.db.add(user)
        self.db.commit()
        
        self.assertEqual(user.id, 1)
      
    def test_create_skill(self):
        skill = Skill('Skiing', None)
        self.db.add(skill)
        self.db.commit()
        
        self.assertEqual(skill.id, 1)
        
if __name__ == '__main__':
    unittest.main()