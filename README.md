# Splott bins

Queries the Cardiff Council's [bin collection website](https://www.cardiff.gov.uk/ENG/resident/Rubbish-and-recycling/When-are-my-bins-collected/Pages/default.aspx) and produces tweets that are posted on the evening of bin night, including what bins need to go out.

The code is written with the intention of being deployed to Heroku and scheduled with redis.

# Installation and usage
```
pip install -r requirements.txt
```
You will need to create a file named `credentials.py` which contains the following key-value pairs from a Twitter App:
```
consumer_key = 'YOUR_KEY'
consumer_secret = 'YOUR_SECRET'
access_token = 'YOUR_TOKEN'
access_token_secret = 'YOUR_TOKEN_SECRET'
```
I followed this [guide](https://www.digitalocean.com/community/tutorials/how-to-create-a-twitter-app#step-2-%E2%80%94-modify-your-application%E2%80%99s-permission-level-and-generate-your-access-tokens) to help me get these values.

Next create a file called `address.csv`. The file should simply contain the first line of the address required, e.g.:
```
18 Copperfield Drive
```
However, it's a bit more complicated than that currently - you also need to modify the `data` component of the POST request based on some values that the website uses to disambiguate the address using, I think, its easting and northing coordinates. I haven't been able to automate this yet so that you can simply put in the address and it works straight away, but I'll try and fix it in the future. A long-winded workaround is to monitor the AJAX requests on the Council site above and copy the data header in the POST request into the requests call in `query_council.py`

To get the bin collection data from the Council website:
```
python query_council.py
```
Then tweet if today is the day before one of the collection days:
```
python produce_tweets.py
```
I have used redis to schedule the scripts (`clock.py` and `worker.py`) according to [this](https://bigishdata.com/2016/12/15/running-python-background-jobs-with-heroku/) guide. The code has been deployed to Heroku (see `Procfile`) successfully and so should work straight off (once you've checked you get sensible data back from `query_council.py`).

# Twitter
The Twitter account which tweets data taken from the Council website is here:
https://twitter.com/splott_bins
