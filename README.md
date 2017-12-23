# ping_gmail

Send emails to POP3 accounts to force gmail to check them more often

Python 3.6+ only, because f-strings are so much fun that a single usage is worth the version constraint.

## Problem

Gmail only checks POP3 accounts as often as it thinks they need to be checked.
If it checks an account and finds no new emails, it waits longer before checking it again: conversely, if it does find new emails, it will check sooner next time (up to maximum of once every 2 minutes).

This is not acceptable for accounts which receive irregular time-sensitive emails.

## Solution

If you're set on using Gmail / Inbox as your mail client, the hacky solution is to pepper your POP3 accounts with emails so often that Gmail always finds new emails.
Then have Gmail set up a filter so that you never actually see these emails.

This script uses GMail's python API to send those keepalive emails to any number of email addresses.

## Filter


```
Matches: from:(<your_sender@email.com>) subject:(Keepalive email)
Do this: Mark as read, Delete it, Never send it to Spam
```

## Code

The code mainly comes from two Google guides:

1. https://developers.google.com/gmail/api/quickstart/python

2. https://developers.google.com/api-client-library/python/start/installation

I've just made it python 3 compatible and filled in all the imports which Google helpfully left out of their guide.

## Usage

Follow guide [1] to get your `client_secret.json` associated with the sender address.

Create your own `addresses_secret.json` with your sender and recipient addresses.

Install the requirements with `pip install -r requirements.txt`

Add this script to your cron daemon with `crontab -e`, and adding this line:

    */2 * * * * /path/to/python /path/to/repo/ping_gmail.py
