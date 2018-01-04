import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

import tweepy
from time import sleep
from credentials import *

r = requests.post("https://wastemanagementcalendar.cardiff.gov.uk/AddressSearch.aspx",
    data='ScriptManager1=UpdatePanel1%7CbtnSearch&__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUINTkyNjYzODIPZBYCAgEPZBYGAgMPZBYCZg9kFgQCCQ8PFgIeC1Bvc3RCYWNrVXJsBQ5%2BL0VuZ2xpc2guYXNweGRkAgsPZBYCZg9kFgICAw8QZGQWAGQCBw88KwARAQwUKwAAZAIJD2QWAmYPZBYCAgEPZBYCZg9kFgICAQ9kFgICAQ9kFgJmD2QWAgIDD2QWAgIBD2QWAgIBD2QWAmYPZBYEAgcPZBYCAgMPEGRkFgFmZAIJD2QWAgIDDxBkZBYBZmQYAQUJR3JpZFZpZXcxD2dkbzYIVPwDTI7TJ%2BYkCtu2aNQVQ4r1M9%2BwFlIWCMy14D4%3D&__VIEWSTATEGENERATOR=B98B31EF&__PREVIOUSPAGE=vRoET5o8n9C72_frMgxzVi5rRPjjygE2Lf6Mu9XYsXMnVtLKTQ_x0QyfCZC8r-VzGoLnFYxKtlu0v9TV56TSwmTR8EwAhlJYz0NRO2IdUHI1&__EVENTVALIDATION=%2FwEdAAW7GET92NTL3L1x4ntO%2BpKqmo%2BdHUlcYdaxxI%2FU%2FS9ZXW8rMPcp2uUNKS9mSvt%2BTTCO1N1XNFmfsMXJasjxX85jjtvMmEKuzieXB%2FWRITu4EIx6kbOo0nZ9p5A6yjLC5Po0qsZ4HWeCy6yN4fFXXXx0&txtAddress=222%20railway%20street&TextBoxWatermarkExtender1_ClientState=&__ASYNCPOST=true&btnSearch=Search',
    headers={
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://wastemanagementcalendar.cardiff.gov.uk",
        "Referer": "https://wastemanagementcalendar.cardiff.gov.uk/AddressSearch.aspx",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
        "X-MicrosoftAjax": "Delta=true",
        "X-Requested-With": "XMLHttpRequest"
    },
    cookies={
        "ASP.NET_SessionId": "b44pktlqhj1lpqmitquh304n",
        "_ga": "GA1.3.1850561422.1452107231"
    },
)

c = r.content

soup = BeautifulSoup(c, "html5lib")

table = soup.find('table', attrs={'class':'border'})

table_body = table.find('tbody')

rows = table_body.find_all('tr')

data = []

for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

tweet_data = []
for ele in data[1:]:
    tweet_dict = {}
    tweet_dict['date'] = datetime.strptime(ele[0],'%A%d/%m/%Y')
    tweet_dict['items'] = []
    for item in ele[2:]:
        item_temp = re.findall('[A-Z][^A-Z]*', item)
        item_temp = [word.upper() for word in item_temp]
        item_temp = ' '.join(item_temp)
        tweet_dict['items'].append(item_temp)
    tweet_dict['items'] = " and ".join(tweet_dict['items'])
    tweet_dict['text'] = 'It\'s bin night in Splott! You need to put out {}'.format(tweet_dict['items'] )
    tweet_data.append(tweet_dict)

consumer_secret = consumer_secret.strip('\t')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

api.update_status(tweet_data[0]['text'])
