import os
import base64
import time

ALLOWED_DOMAINS = ["accenture.com", "cognizant.com", "quest-global.com", "nestgroup.net"]
ALLOWED_EMAILS = [
    "anoop.p.stanley@gmail.com", 
    "stanley.anoop@gmail.com", 
    "seenusimpsontvm@gmail.com", 
    "vinoop.p.stanley@gmail.com",
    "writetostanleyj@gmail.com",
    "sanusimpson@gmail.com",
    "ksfekesavadasapuram@gmail.com",
    "15@ksfe.com",
    ]
ALLOWED_KEYWORDS = [
    "60xxxx322", "60XXXX322",
    "**1953",
    "XXXXXXXXXX1953", "xxxxxxxxxx1953",
    "603067322",
    "64/2022/A/4-156",
    "64/2022/A/4-155",
    "AIJPA8209N",
    "Action Required:"
]

class GmailUtil:
    '''
    Utility class for Gmail operations.
    This class provides methods to authenticate with the Gmail API, list messages, analyze content,
    and process messages based on allowed keywords and domains.
    It uses the Gmail API to interact with the user's Gmail account.
    '''
    def __init__(self, service):
        self.service = service
    
    def list_all_messages(self, service, user_id='me', query=None):
        all_messages = []
        next_page_token = None

        while True:
            response = service.users().messages().list(
                userId=user_id,
                q=query,
                pageToken=next_page_token,
                maxResults=500  # max allowed by Gmail API
            ).execute()

            if 'messages' in response:
                all_messages.extend(response['messages'])

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        return all_messages
    
    def analyze_content(self, text):
        """ 
        Analyze the content of the email body (text) and responds with a boolean.
        This function checks if the text contains any allowed keywords. 
        If it does, it returns False (indicating the email should not be deleted).
        If it does not contain any allowed keywords, it returns True (indicating the email can be deleted).
        """
        if any(keyword.lower() in text.lower() for keyword in ALLOWED_KEYWORDS):
            print(f"Skipping content; as it contains at least one of the allowed keywords: {ALLOWED_KEYWORDS}.")
            return False
        return True
    
    def process_message(self, service, messages):
        '''
        Process each message and delete it if it does not contain any allowed keywords or is from an allowed domain/email.
        This function iterates through the list of messages, checks the subject and sender's email address,
        and decides whether to delete the message based on the allowed keywords and domains.
        It prints the subject and sender's email address for each message, and if the message is deleted,
        it prints a confirmation message.
        '''
        total_messages = len(messages)
        print (f"Number of messages to process: {total_messages}")
        count = 0
        for msg in messages:
            try:
                print(f"{'*'* 100}\n{'*' * 100}\n")
                skip_msg = False
                msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
                payload = msg_data['payload']
                headers = payload.get('headers', [])
                for header in headers:
                    if header['name'].lower() == 'subject':
                        subject = header['value']
                        print(f"Subject >>>>> {subject}") 
                        if any(keyword.lower() in subject.lower() for keyword in ALLOWED_KEYWORDS):
                            print(f"Skipping email; as it contains at least one of the allowed keywords: {ALLOWED_KEYWORDS}.")
                            skip_msg = True
                            break
                    elif header['name'].lower() == 'from':
                        from_email = header['value']
                        sender_domain = from_email.split('@')[-1] if from_email else None
                        sender_domain = sender_domain[0:sender_domain.index('>')] if '>' in sender_domain else sender_domain
                        print (f"From Email >>>>> {from_email, ALLOWED_EMAILS}")
                        print (f"Domain     >>>>> {sender_domain, ALLOWED_DOMAINS}")
                        if sender_domain in ALLOWED_DOMAINS or any(email in from_email for email in ALLOWED_EMAILS):
                            print(f"Skipping email; as it is from allowed domain  ({sender_domain}) or allowed email ({from_email}).")
                            skip_msg = True
                            break
                        print(f"From: {from_email, sender_domain}")
                if skip_msg:
                    print("Skipping this email as it's either from an allowed domain/mail id or it contains allowed keywords.")
                    continue
                print (f"Analyzing email from: {from_email}, with  subject: {subject}")
                parts = payload.get('parts', [])
                email_body = ""

                # Extract text from email
                if parts:
                    for part in parts:
                        if part['mimeType'] == 'text/plain':
                            email_body = base64.urlsafe_b64decode(part['body']['data']).decode()
                            break
                else:
                    email_body = base64.urlsafe_b64decode(payload['body']['data']).decode()

                if self.analyze_content(email_body):
                    count += 1
                    print (f"Analysis is done, and found to be okay to delete. Delete permanently : {count}")
                    if count % 500 == 0:
                        print(f"{'^' * 100}\n{'*' * 100}\n \t\t\tA Short 5 sec Coffee Break c\\_/ ~~\n{'*' * 100}\n{'v' * 100}\n")
                        time.sleep(5)
                    if count == 10000:
                        print("Reached 10,000 messages. Stopping further deletion to avoid rate limits.")
                        break
                    service.users().messages().delete(userId='me', id=msg['id']).execute()
                    print(f"Deleted email {msg['id']}")
            except Exception as e:
                print(f"An error occurred while processing message {msg['id']}: {e}\nSkipping this message and continuing with the next one.")
                continue
        print (f"Total messages Deleted: {count} out of {total_messages}.")
        print (f"{total_messages - count} messages were skipped as they were either from allowed domains/email or contained allowed keywords or it reached the threshold.")


