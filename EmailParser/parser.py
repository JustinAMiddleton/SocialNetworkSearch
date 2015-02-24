import os
import re
import threading    # could need for multithreading, not used yet. here is some threading info http://stackoverflow.com/questions/1190206/threading-in-python
from nltk.tokenize import sent_tokenize
from dbFacade import dbFacade

def searchEnron(wordDeck, db):

	# Ubuntu
	emailMainDirectory = r'/users/lukelindsey/Downloads/enron_mail_20110402/maildir/'
	
	# Windows
	emailMainDirectory = "C:\\Users\\Brenden\\Downloads\\enron\\enron_mail_20110402\\maildir\\"
	
	mySentFolder = r'/sent/'

	for userDir in os.listdir(emailMainDirectory):
		for sentFolder, noDirectories, emailFiles in os.walk(emailMainDirectory + userDir + mySentFolder):  # there are more sent folders than this, let's start small though
			#print userDir  # this is the user that sent the email, printing to make sure all folders are being searched, remove later
			for emailFileName in emailFiles:
				emailFile = open((sentFolder + emailFileName), 'r')
				email = emailFile.read()
				emailFile.close()
				processEmail(email, userDir, wordDeck)

def processEmail(email, user, wordDeck):
    #make sure we only get the part of email we want
    email = formatEmail(email)
	
    for word in wordDeck:
        if word in email:
            sentences = extractSentences(word, email)
            for sentence in sentences:
                if word in sentence:
					print sentence
					db.add_post(user, "Enron", sentence, word)

"""This method returns a generator of sentences that contain the
word passed in as a parameter"""
def extractSentences(wordIn, emailIn):
    sentenceList = sent_tokenize(emailIn)
    for sentence in sentenceList:
        if wordIn in sentence:
            yield sentence

def formatEmail(text):
	'''@ GITHUB -> inkhorn / enron processing.py '''
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
	text = text.replace("-----Original Message-----","")

	# remove some excessive whitespace
	text = text.replace('\n', ' ')
	text = text.replace('  ', ' ')

	return text
	
# DATABASE PREPERATION
db = dbFacade()
db.connect()
db.create_keyspace_and_schema()

try:
	searchEnron(['random'], db) # just a placeholder for now
except KeyboardInterrupt:
	print "\n\tTerminated by user"