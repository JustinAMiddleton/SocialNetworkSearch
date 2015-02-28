import re

"""
The purpose of this file is to 'clean' the emails
of anything but the actual main body of the email.
This includes removing 'original messages' and tags
that are in the header of each email file.
"""

def format_email(email):
	email = remove_tags(email)
	email = remove_forwards(email)
	email = remove_replies(email)
	return email

def remove_tags(email):
	"""@ GITHUB -> inkhorn / enron processing.py """
	# remove headers
	email = email[email.find("\n\n"):]

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
	email = to_pat.sub('', email)
	email = cc_pat.sub('', email)
	email = subject_pat.sub('', email)
	email = from_pat.sub('', email)
	email = sent_pat.sub('', email)
	email = email_pat.sub('', email)
	email = ctype_pat.sub('', email)
	email = reply_pat.sub('', email)
	email = date_pat.sub('', email)
	email = xmail_pat.sub('', email)
	email = mimver_pat.sub('', email)
	email = contentinfo_pat.sub('', email)
	email = forwardedby_pat.sub('', email)
	email = caution_pat.sub('', email)
	email = privacy_pat.sub('', email)
	email = email.replace("-----Original Message-----", "")

	# remove some excessive whitespace
	email = email.replace('\n', ' ')
	email = email.replace('  ', ' ')

	return email


def remove_forwards(email):
	"""
	Purpose of this method is to remove forwarded emails from
	the email file sent in.
	"""
	return email


def remove_replies(email):
	"""
	Removes the emails that are listed below what the user actually
	sent (i.e. messages they've replied to).
	"""
	return email