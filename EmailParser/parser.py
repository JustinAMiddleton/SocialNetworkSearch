import os
import re
from nltk.tokenize import sent_tokenize
from dbFacade import dbFacade


def search_enron(word_deck, db, email_main_directory='/users/lukelindsey/Downloads/enron_mail_20110402/maildir/'):

	# Windows (Brenden's machine)
	if os.name == 'nt':
		email_main_directory = "C:\\Users\\Brenden\\Downloads\\enron\\enron_mail_20110402\\maildir\\"
	
	my_sent_folder = r'/sent/'  # there are more sent folders than this, let's start small though

	user_directory_list = os.listdir(email_main_directory)

	for user_dir in user_directory_list:
		for sent_folder, no_directories, email_files in os.walk(email_main_directory + user_dir + my_sent_folder):
			for email_file_name in email_files:
				email_file = open((sent_folder + email_file_name), 'r')
				email = email_file.read()
				email_file.close()
				process_email(email, user_dir, word_deck)


def process_email(email, user, word_deck):

	email = format_email(email)  # remove the junk

	for word in word_deck:
		if word in email:
			sentences = extract_sentences(word, email)
			for sentence in sentences:
				if word in sentence:
					#score here?
					db.add_post(user, "Enron", sentence, word)


def extract_sentences(word_to_search, email):
	"""This method returns a generator of sentences that contain the
	word passed in as a parameter"""

	sentence_list = sent_tokenize(email)
	for sentence in sentence_list:
		if word_to_search in sentence:
			yield sentence


def format_email(text):
	"""@ GITHUB -> inkhorn / enron processing.py """
	# remove headers
	text = text[text.find("\n\n"):]

	# regular expression declaration
	email_pat = re.compile(".+@.+")
	to_pat = re.compile("To:.+\n")
	cc_pat = re.compile("cc:.+\n")
	subject_pat = re.compile("Subject:.+\n")
	from_pat = re.compile("From:.+\n")
	sent_pat = re.compile("Sent:.+\n")
	received_pat = re.compile("Received:.+\n")
	ctype_pat = re.compile("Content-Type:.+\n")
	reply_pat = re.compile("Reply- Organization:.+\n")
	date_pat = re.compile("Date:.+\n")
	xmail_pat = re.compile("X-Mailer:.+\n")
	mimver_pat = re.compile("MIME-Version:.+\n")
	contentinfo_pat = re.compile("----------------------------------------.+----------------------------------------")
	forwardedby_pat = re.compile(".+------------.+\n")
	caution_pat = re.compile('''\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*.+\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*''')
	privacy_pat = re.compile(" _______________________________________________________________.+ _______________________________________________________________")

	# regular expression cleanup
	text = to_pat.sub('', text)
	text = cc_pat.sub('', text)
	text = subject_pat.sub('', text)
	text = from_pat.sub('', text)
	text = sent_pat.sub('', text)
	text = email_pat.sub('', text)
	text = ctype_pat.sub('', text)
	text = reply_pat.sub('', text)
	text = date_pat.sub('', text)
	text = xmail_pat.sub('', text)
	text = mimver_pat.sub('', text)
	text = contentinfo_pat.sub('', text)
	text = forwardedby_pat.sub('', text)
	text = caution_pat.sub('', text)
	text = privacy_pat.sub('', text)
	text = text.replace("-----Original Message-----", "")

	# remove some excessive whitespace
	text = text.replace('\n', ' ')
	text = text.replace('  ', ' ')

	return text
	
# DATABASE PREPERATION
db = dbFacade()
db.connect()
db.create_keyspace_and_schema()

try:
	search_enron(['random'], db)  # just a placeholder for now
except KeyboardInterrupt:
	print "\n\tTerminated by user"