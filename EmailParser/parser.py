import os
import threading    # will need for multithreading, not used yet


def main(wordDeck):
    emailMainDirectory = '/users/lukelindsey/Downloads/enron_mail_20110402/maildir/'
    for userDir in os.listdir(emailMainDirectory):
        for sentFolder, noDirectories, emailFiles in os.walk(emailMainDirectory + userDir + '/sent/'):  # there are more sent folders than this, let's start small though
            print userDir  # this is the user that sent the email
            for emailFileName in emailFiles:
                emailFile = open((emailMainDirectory + userDir + '/sent/' + emailFileName), 'r')
                email = emailFile.read()
                print email
                # for word in wordDeck:
                    # if word in email:
                        #************ FIND SENTENCE WHERE WORD IS USED
            # dashes separate users while we are printing, take this out when useful stuff is done
            print '---------------------------------------------------------------------'


main(['this']) # just a placeholder for now