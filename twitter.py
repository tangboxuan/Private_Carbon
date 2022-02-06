from cgitb import lookup
from http.client import FORBIDDEN
from decouple import config
import tweepy
import co2
import time

customer_key        = config("CKEY")
customer_secret     = config("CSECRET")
access_token        = config("ATOKEN")
access_token_secret = config("ASECRET")
bearer              = config("BEARER")

client = tweepy.Client(
    bearer_token=bearer,
    consumer_key=customer_key,
    consumer_secret=customer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

def tweet(reply):
    emissions = co2.getco2(client)
    client.create_tweet(text="Hey Elon Musk's private jet had " + emissions + " pounds of emissions in the last 30 days", in_reply_to_tweet_id=reply)

lookup = {"environment"}

while True:
    time.sleep(5)
    userId = client.get_user(username="demo_jet_owner").data.id
    latest_tweet = client.get_users_tweets(userId, max_results=5).data[0]
    latest_tweet_id = latest_tweet.id
    print(latest_tweet)
    f = open("latest.txt", "r")
    if not f.read().strip() == latest_tweet_id:
        toreply = False
        for word in str(latest_tweet).lower().split():
            if word in lookup:
                toreply = True
        print(toreply)
        if toreply:
            try:
                tweet(latest_tweet_id)
                with open("latest.txt", "w") as f2:
                    f2.write(str(latest_tweet_id))
                print("posted tweet")
            finally:
                continue
    f.close()
