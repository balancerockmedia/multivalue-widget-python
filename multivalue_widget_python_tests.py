import os
from flaskext.sqlalchemy import SQLAlchemy
import multivalue_widget_python as mvp
import unittest

class AppTestCase(unittest.TestCase):
    
    def setUp(self):
        mvp.app.config['TESTING'] = True
        
        mvp.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:@127.0.0.1:3306/multivalue_widget_test'
        
        self.app = mvp.app.test_client()
        
        mvp.db.create_all()
        
    def tearDown(self):
        mvp.db.drop_all()
        
    def test_create_user(self):
        user = mvp.User('Dan', 'Johnson')
        mvp.db.session.add(user)
        mvp.db.session.commit()
        
        self.assertEqual(user.id, 1)
        
if __name__ == '__main__':
    unittest.main()