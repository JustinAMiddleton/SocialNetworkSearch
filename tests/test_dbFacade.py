import unittest
from SocialNetworkSearch.dbFacade import dbFacade

class test_dbFacade(unittest.TestCase):

	def test_firstTest(self):
		db = dbFacade()
		db.connect()

if __name__ == '__main__':
    unittest.main()
