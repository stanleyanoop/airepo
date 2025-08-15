from __future__ import print_function
import sys
import base64
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from gmail_util import GmailUtil
import re

# Gmail API scopes
SCOPES = ['https://mail.google.com/']
test = False # Set to False for production mode (bulk delete), True for test mode (just list 100 messages)

# print (sys.path)

def authenticate_gmail():
    '''
    Authenticate the user and return the Gmail service.
    This function uses OAuth2 to authenticate the user and returns a service object to interact with the Gmail API.
    It checks for existing credentials in 'credentials.json' and refreshes them if necessary.
    If no valid credentials are found, it prompts the user to log in and grants access to their Gmail account.
    '''
    creds = None
    if os.path.exists('token.json'):
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def main():
    service = authenticate_gmail()
    util = GmailUtil(service)
    if test:
        print("Running in test mode. Only listing 100 messages without deletion.")
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])
    else:
        print ("Running in production mode. Deleting messages after analysis.")
        messages = util.list_all_messages(service, user_id='me')
    
    print(f"Found {len(messages)} potential messages to be deleted.")

    if not messages:
        print("No messages.")
        return
    util.process_message(service, messages)
    print("Processing completed.")

if __name__ == '__main__':
    main()