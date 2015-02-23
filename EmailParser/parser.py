import os
import threading    # could need for multithreading, not used yet. here is some threading info http://stackoverflow.com/questions/1190206/threading-in-python
from nltk.tokenize import sent_tokenize

def main(wordDeck):

    emailMainDirectory = r'/users/lukelindsey/Downloads/enron_mail_20110402/maildir/'
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
    email = formatEmail(email) #this does nothing right now

    for word in wordDeck:
        if word in email:
            sentences = extractSentences(word, email)
            for sentence in sentences:
                if word in sentence:
                    pass #PLACEHOLDER
                    #send sentence, word (query), and user to the db

"""This method returns a generator of sentences that contain the
word passed in as a parameter"""
def extractSentences(wordIn, emailIn):
    sentenceList = sent_tokenize(emailIn)
    for sentence in sentenceList:
        if wordIn in sentence:
            yield sentence

def formatEmail(email):
    return email


main(['random']) # just a placeholder for now