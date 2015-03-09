import unittest
import EmailParser.emailformat as ef

"""__author__ = 'LukeLindsey' """

class test_emailformat(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.email_main_dir = '/users/lukelindsey/Downloads/enron_mail_20110402/maildir/'

	# format_email tests
	def test_format_email_with_tags_only(self):
		expected = '\r\nyes'
		email_file = open((self.email_main_dir + 'carson-m' + '/sent/' + '8.'), 'r')
		email = email_file.read()
		email = ef.format_email(email)
		self.assertEquals(expected, email)

	def test_format_email_with_forward_only(self):
		expected = '\r\n'
		email_file = open((self.email_main_dir + 'allen-p' + '/sent/' + '2.'), 'r')
		email = email_file.read()
		email = ef.format_email(email)
		self.assertEquals(expected, email)

	def test_format_email_with_reply(self):
		email_file = open((self.email_main_dir + 'arnold-j' + '/sent/' + '9.'), 'r')
		email = email_file.read()
		expected = email[448:679]
		email = ef.format_email(email)
		self.assertEquals(expected, email)

	def test_format_email_with_mix_reply_first(self):
		email_file = open((self.email_main_dir + 'arnold-j' + '/sent/' + '82.'), 'r')
		email = email_file.read()
		expected = email[445:597]
		email = ef.format_email(email)
		self.assertEquals(expected, email)

	def test_format_email_with_mix_forward_first(self):
		email_file = open((self.email_main_dir + 'bass-e' + '/sent/' + '161.'), 'r')
		email = email_file.read()
		expected = email[416:459]
		email = ef.format_email(email)
		self.assertEquals(expected, email)

	def test_format_email_with_more_forwards(self):
		pass

	def test_format_email_with_more_replies(self):
		email_file = open((self.email_main_dir + 'arnold-j' + '/sent/' + '118.'), 'r')
		email = email_file.read()
		expected = email[428:702]
		email = ef.format_email(email)
		self.assertEquals(expected, email)

	def test_format_email_external_reply(self):
		email_file = open((self.email_main_dir + 'arnold-j' + '/sent/' + '25.'), 'r')
		email = email_file.read()
		expected = email[454:569]
		email = ef.format_email(email)
		self.assertEquals(expected, email)


	# remove_tags tests
	def test_remove_tags_very_small_remaining(self):
		expected = '\r\nyes'
		email_file = open((self.email_main_dir + 'carson-m' + '/sent/' + '8.'), 'r')
		email = email_file.read()
		email = ef.remove_tags(email)
		self.assertEquals(expected, email)

	def test_remove_tags_forward_and_reply_below(self):
		email_file = open((self.email_main_dir + 'bass-e' + '/sent/' + '161.'), 'r')
		email = email_file.read()
		expected = email[416:len(email)]
		email = ef.remove_tags(email)
		self.assertEquals(expected, email)

	def test_remove_tags_external_reply_below(self):
		email_file = open((self.email_main_dir + 'arnold-j' + '/sent/' + '25.'), 'r')
		email = email_file.read()
		expected = email[454:len(email)]
		email = ef.remove_tags(email)
		self.assertEquals(expected, email)

	# remove_forwards tests
	def test_remove_forward_none_remaining(self):
		email_file = open((self.email_main_dir + 'allen-p' + '/sent/' + '2.'), 'r')
		email = email_file.read()
		expected = email[0:484]
		email = ef.remove_forwards(email)
		self.assertEquals(expected, email)

	def test_remove_forwards_with_mix_forward_first(self):
		email_file = open((self.email_main_dir + 'bass-e' + '/sent/' + '161.'), 'r')
		email = email_file.read()
		expected = email[0:459]
		email = ef.remove_forwards(email)
		self.assertEquals(expected, email)

	# remove_replies tests
	def test_remove_reply_external_name_time_same_line(self):
		email_file = open((self.email_main_dir + 'arnold-j' + '/sent/' + '9.'), 'r')
		email = email_file.read()
		expected = email[0:679]
		email = ef.remove_replies(email)
		self.assertEquals(expected, email)

	def test_remove_reply_external_reply_with_quotes(self):
		email_file = open((self.email_main_dir + 'arnold-j' + '/sent/' + '25.'), 'r')
		email = email_file.read()
		expected = email[0:569]
		email = ef.remove_replies(email)
		self.assertEquals(expected, email)

	def test_remove_reply_mix_reply_first(self):
		email_file = open((self.email_main_dir + 'arnold-j' + '/sent/' + '82.'), 'r')
		email = email_file.read()
		expected = email[0:597]
		email = ef.remove_replies(email)
		self.assertEquals(expected, email)

	def test_remove_replies_multiple_to_format(self):
		email_file = open((self.email_main_dir + 'arnold-j' + '/sent/' + '118.'), 'r')
		email = email_file.read()
		expected = email[428:702]
		email = ef.remove_replies(email[428:len(email)])
		self.assertEquals(expected, email)