from decouple import config
import tweepy
from dateutil.parser import *
from datetime import datetime, timedelta
import re

customer_key        = config("CKEY")
customer_secret     = config("CSECRET")
access_token        = config("ATOKEN")
access_token_secret = config("ASECRET")
bearer              = config("BEARER")

dt = datetime.now() - timedelta(days=30)
dt_str = dt.strftime("%Y-%m-%dT%H:%M:%S.%SZ")
client = tweepy.Client(
    bearer_token=bearer,
    consumer_key=customer_key,
    consumer_secret=customer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)
userId = client.get_user(username="ElonJet").data.id
tweets = client.get_users_tweets(userId, max_results=100, start_time=dt_str)
total = 0
for tweet in tweets.data:
    words = []
    for word in str(tweet).split():
        if not word.startswith("http"):
            words.append(word)
    words = ''.join(words)
    nums = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", words)
    if len(nums) == 1 and int(nums[0]) < 60:
        mins = int(nums[0])
    elif len(nums) == 2 and int(nums[0]) < 12 and int(nums[1]) < 60:
        mins = int(nums[0]) * 60 + int(nums[1])
    else:
        mins = 0
    total += mins
co2 = (total/60*10614)
print(co2)
client.create_tweet(text="Hey Elon Musk's private jet had " + str(co2) + " of emissions in the last 30 days")

