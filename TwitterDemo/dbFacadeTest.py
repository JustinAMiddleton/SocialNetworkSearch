import unittest
import time
from dbFacade import dbFacade

class dbFacadeTest(unittest.TestCase):
	
	def setUp(self):
		self.db = dbFacade()
		self.db.connect()
		self.db.create_keyspace_and_schema()
		
	def tearDown(self):
		self.db.session.execute("DROP KEYSPACE %s;" % self.db.keyspace)
		time.sleep(1)
		self.db.close()		
		
	#def test(self):
	#	pass
		
	def test_add_post(self):
		self.db.add_post('tammy', 'Twitter', 'mooreadfa', 'Dogs')
		results = self.db.session.execute("SELECT * FROM %s.posts;" % self.db.keyspace)
		self.assertTrue(len(results) > 0)
		
if __name__ == '__main__':
	unittest.main()