# Splott bins

Queries the Cardiff Council's bin collection data and produces tweets that are posted on the evening of bin night, including what bins need to go out.

# Installation
```
pip install -r requirements.txt
```

# Usage
First get the bin collection data from the Council website:
```
python query_council.py
```

Then tweet if today is the day before one of the collection days:

```
python product_tweets.py
```

# Twitter
https://twitter.com/splott_bins
