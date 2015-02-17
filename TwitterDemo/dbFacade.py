from cassandra.cluster import Cluster
import cassandra.cluster
import time
import uuid

class dbFacade(object):
	session = None
	keyspace = None
	
	def connect(self):
		while(True):
			try:
				cluster = Cluster(['131.204.27.98'])
				self.session = cluster.connect()
				break;
			except cassandra.cluster.NoHostAvailable:
				print "Connection failed, retrying.."
				time.sleep(1)
			except Exception as e:
				print str(e)
				time.sleep(1)
		print "Connected to cassandra database."
		
	def close(self):
		time.sleep(1)
		self.session.cluster.shutdown()
		self.session.shutdown()
		
	def add_user(self, username, score, website):
		self.session.execute("""
			INSERT INTO %s.users (username, score, website)
			VALUES ('%s', %s, '%s'); 
			""" % (self.keyspace, username, score, website))
			
	def add_post(self, username, website, content, query):	
		self.session.execute("""
			INSERT INTO %s.posts (id, username, website, content, query)
			VALUES (%s, '%s', '%s', '%s', '%s');
			""" % (self.keyspace, uuid.uuid1(), username, website, content, query))
	
	def get_users(self):
		results = self.session.execute("""
				SELECT * FROM %s.users;
				""" % self.keyspace)
		return results
		
	def create_keyspace_and_schema(self):
		timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")
		self.keyspace = "search_%s" % timestamp

		self.session.execute("""
			CREATE KEYSPACE %s WITH
			replication = {'class':'SimpleStrategy','replication_factor':3};
			""" % self.keyspace)
		
		self.session.execute("""
			CREATE TABLE %s.users (
				username text,
				score int,
				website text,
				PRIMARY KEY (username, score)
			) WITH CLUSTERING ORDER BY (score DESC);
			""" % self.keyspace)
		
		self.session.execute("""
			CREATE TABLE %s.posts (
				id uuid,
				username text,
				website text,
				content text,
				query text,
				PRIMARY KEY (id, username)	
			);
			""" % self.keyspace)
			
def main():
	db = dbFacade()
	db.connect()
	
	print "Connected."
	
	db.create_keyspace_and_schema()
	print "Schema created"
	time.sleep(1)
	db.add_user('tom', 105, "Twitter")
	print "Inserted"
	time.sleep(1)
	db.get_users()
	time.sleep(1)
	db.close()

if __name__ == "__main__":
	main()