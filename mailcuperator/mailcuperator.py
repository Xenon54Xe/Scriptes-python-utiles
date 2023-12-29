import imaplib
import email
from email.header import decode_header
import webbrowser
import os

# account credentials
username = "email@example.com"
password = "***********"
# use your email provider's IMAP server, you can look for your provider's IMAP server on Google
# or check this page: https://www.systoolsgroup.com/imap/
# for yahoo, it's this:
imap_server = "imap.mail.yahoo.com"


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


# create an IMAP4 class with SSL
imap = imaplib.IMAP4_SSL(imap_server)
# authenticate
imap.login(username, password)


test = imap.list()
print(test)
"""
status, messages = imap.select("INBOX")
# number of top emails to fetch
N = 3
# total number of emails
messages = int(messages[0])
"""
