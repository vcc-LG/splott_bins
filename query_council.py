import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import _pickle as cPickle
import pprint
import sys
import csv
import logging

logging.basicConfig(filename="query_log.log", level=logging.DEBUG)

def post_request(address_details):
    r = requests.post("https://wastemanagementcalendar.cardiff.gov.uk/AddressSearch.aspx",
        data='ScriptManager1=UpdatePanel1%7CbtnSearch&__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUINTkyNjYzODIPZBYCAgEPZBYGAgMPZBYCZg9kFgQCCQ8PFgIeC1Bvc3RCYWNrVXJsBQ5%2BL0VuZ2xpc2guYXNweGRkAgsPZBYCZg9kFgICAw8QZGQWAGQCBw88KwARAQwUKwAAZAIJD2QWAmYPZBYCAgEPZBYCZg9kFgICAQ9kFgICAQ9kFgJmD2QWAgIDD2QWAgIBD2QWAgIBD2QWAmYPZBYEAgcPZBYCAgMPEGRkFgFmZAIJD2QWAgIDDxBkZBYBZmQYAQUJR3JpZFZpZXcxD2dkbzYIVPwDTI7TJ%2BYkCtu2aNQVQ4r1M9%2BwFlIWCMy14D4%3D&__VIEWSTATEGENERATOR=B98B31EF&__PREVIOUSPAGE=vRoET5o8n9C72_frMgxzVi5rRPjjygE2Lf6Mu9XYsXMnVtLKTQ_x0QyfCZC8r-VzGoLnFYxKtlu0v9TV56TSwmTR8EwAhlJYz0NRO2IdUHI1&__EVENTVALIDATION=%2FwEdAAW7GET92NTL3L1x4ntO%2BpKqmo%2BdHUlcYdaxxI%2FU%2FS9ZXW8rMPcp2uUNKS9mSvt%2BTTCO1N1XNFmfsMXJasjxX85jjtvMmEKuzieXB%2FWRITu4EIx6kbOo0nZ9p5A6yjLC5Po0qsZ4HWeCy6yN4fFXXXx0&txtAddress={}&TextBoxWatermarkExtender1_ClientState=&__ASYNCPOST=true&btnSearch=Search'.format(address_details[0].replace(' ','%20')),
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
    try:
        r.raise_for_status()
        print("Connected successfully to Council website")
        return r
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print ("General requests error",err)
        sys.exit(1)

def parse_content(response):
    c = response.content
    soup = BeautifulSoup(c)
    table = soup.find('table', attrs={'class':'border'})
    try:
        table_body = table.find('tbody')
    except:
        print("Could not find table in HTML - is your address file correct?")
        sys.exit(1)
    rows = table_body.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    return data

def create_tweets_dict(raw_data):
    tweet_data = []
    for ele in raw_data[1:]:
        tweet_dict = {}
        tweet_dict['date'] = datetime.strptime(ele[0],'%A%d/%m/%Y')
        tweet_dict['items'] = []
        for item in ele[1:]:
            item_temp = re.findall('[A-Z][^A-Z]*', item)
            item_temp = [word.upper() for word in item_temp]
            item_temp = ' '.join(item_temp)
            if "NOT CURRENTLY REGISTERED" in item_temp:
                item_temp = item_temp.replace('NOT CURRENTLY REGISTERED.  PLEASE CONTACT US ','')
            tweet_dict['items'].append(item_temp)
        tweet_dict['items'] = " and ".join(tweet_dict['items'])
        tweet_dict['text'] = '{}: It\'s bin night in Splott! You need to put out {}'.format(tweet_dict['date'].strftime("%A, %d. %B %Y"), tweet_dict['items'] )
        tweet_data.append(tweet_dict)
    return tweet_data

def save_data(tweet_data):
    with open('bin_data.p', 'wb') as fp:
        cPickle.dump(tweet_data, fp)
    print('Data saved successfully')
    logging.debug("{} : Successful query and save".format(datetime.now()))

def get_address_details():
    with open('address.csv', 'r') as f:
        reader = csv.reader(f)
        output_list = list(reader)
    return output_list[0]

def run_query_council():
    address_details = get_address_details()
    r = post_request(address_details)
    raw_data = parse_content(r)
    tweet_data = create_tweets_dict(raw_data)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(tweet_data)
    save_data(tweet_data)

if __name__ == "__main__":
    address_details = get_address_details()
    r = post_request(address_details)
    raw_data = parse_content(r)
    tweet_data = create_tweets_dict(raw_data)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(tweet_data)
    save_data(tweet_data)
