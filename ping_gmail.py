#!/usr/bin/env python
"""
To get the credentials to be stored in client_secret.json, follow the guide here:

    https://developers.google.com/gmail/api/quickstart/python

Most of this code is copied from the guide here:

    https://developers.google.com/gmail/api/guides/sending
"""

import os
from datetime import datetime
import json
from email.mime.text import MIMEText
import base64
from urllib.error import HTTPError

import httplib2

from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'
ADDRESSES_PATH = 'addresses_secret.json'

SUBJECT = 'Keepalive email ' + datetime.now().strftime('%c')
MESSAGE_TEXT = 'server status: OK'


with open(ADDRESSES_PATH) as f:
    addresses = json.load(f)

FROM = addresses['from']
TO = addresses['to']


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    os.makedirs(credential_dir, exist_ok=True)
    credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    
    return credentials


def create_message(to, sender=FROM, subject=SUBJECT, message_text=MESSAGE_TEXT):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')}


def send_message(service, message, user_id='me'):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message ID: ' + message['id'])
        return message
    except HTTPError as error:
        print(f'An error occurred: {error}')


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    
    for to in TO:
        msg = create_message(to)
        send_message(service, msg)

if __name__ == '__main__':
    main()
