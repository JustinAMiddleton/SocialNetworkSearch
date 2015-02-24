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
		# Escape single quotes
		content = content.replace("'", "''")
		
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
			
	def clearDatabase(self):
		keyspaces = self.getKeyspaceNames()
		
		for keyspace in keyspaces:
			if "search" in keyspace:
				self.session.execute("""DROP KEYSPACE %s;""" % keyspace)
					
	def getKeyspaceNames(self):
		keys = self.session.execute("""
			SELECT * FROM system.schema_keyspaces;"""); 
			
		keyspaces = []
		for key in keys:
			keyspaces.append(key.keyspace_name)
			
		return keyspaces