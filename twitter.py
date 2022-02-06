from cgitb import lookup
from decouple import config
import tweepy
import co2
import time
from pathlib import Path
import meme

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
    lower = emissions + " pounds of CO2 from private jets in 30 days"
    meme_link = meme.make_meme(str(latest_tweet), lower)
    client.create_tweet(text="Hey @demo_jet_guy, your private jet contributed " 
        + emissions + " pounds of CO2 in the last 30 days " 
        + meme_link + " You could plant " + str(int(emissions)//44) 
        + " trees or offset your carbon footprint here: https://bit.ly/35HEYSe",
        in_reply_to_tweet_id=reply)

lookup = {"environment", "climate", "warming", "renewables", "recycle", "melting", "extinction"}

while True:
    time.sleep(2)
    userId = client.get_user(username="demo_jet_owner").data.id
    latest_tweet = client.get_users_tweets(userId, max_results=5).data[0]
    latest_tweet_id = latest_tweet.id
    
    last_tweet_id_file = Path('latest.txt')
    last_tweet_id = last_tweet_id_file.read_text()
    if not int(last_tweet_id) == latest_tweet_id:
        toreply = False
        upper = []
        for word in str(latest_tweet).lower().split():
            if word in lookup:
                toreply = True
        if toreply:
            try:
                tweet(latest_tweet_id)
                last_tweet_id_file.write_text(str(latest_tweet_id))
                print("posted tweet")
            finally:
                continue
    else:
        print(str(latest_tweet_id) + " already replied")