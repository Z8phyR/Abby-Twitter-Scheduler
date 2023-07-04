import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

# Twitter API credentials
key = os.getenv("TWITTER_API_KEY")
keySecret = os.getenv("TWITTER_API_SECRET")
accessToken = os.getenv("TWITTER_ACCESS_TOKEN")
accessTokenSecret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Bearer token can be None if you're not using one
bearer_token = None

client = tweepy.Client(bearer_token, key, keySecret,
                       accessToken, accessTokenSecret)

# Verify credentials
client.get_me()

# Post a tweet
tweet_text = "Hello, Twitter!"
client.create_tweet(text=tweet_text)
