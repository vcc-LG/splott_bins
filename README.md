# Splott bins

Queries the Cardiff Council's bin collection data and produces tweets that are posted on the evening of bin night, including what bins need to go out.

# Installation
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

# Usage
First get the bin collection data from the Council website:
```
python query_council.py
```

Then tweet if today is the day before one of the collection days:

```
python product_tweets.py
```
You can change the Cardiff region it looks up by modifying the contents of `address.csv`. This isn't entirely reliable though. The file should simply contain the first line of the address required, e.g.:
```
18 Copperfield Drive
```
The code will fail for non-unique Cardiff addresses. There is a way of performing the query using the address's easting and northing values, but I haven't figured out to make this straightforward for users. Just avoid non-unique addresses!


# Twitter
The Twitter account which tweets data taken from the Council website is here:
https://twitter.com/splott_bins

# Hosting
The code will be hosted on PythonAnywhere.
