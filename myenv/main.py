from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import tweepy
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import threading
from bson import ObjectId
import dateparser
import random

# Load environment variables
load_dotenv()

# Twitter API credentials
key = os.getenv("TWITTER_API_KEY")
keySecret = os.getenv("TWITTER_API_SECRET")
accessToken = os.getenv("TWITTER_ACCESS_TOKEN")
accessTokenSecret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# MongoDB credentials
mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB_NAME")

# Connect to Twitter


def connect_to_twitter():
    print("Verifying Twitter credentials...")
    client = tweepy.Client(None, key, keySecret,
                           accessToken, accessTokenSecret)
    user = client.get_me()
    print(f"Logged in as {user.data.username}")
    return client

# Connect to MongoDB


def connect_to_mongodb():
    print("Connecting to MongoDB...")
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client[mongo_db_name]
    tweets = db.tweets
    print("Connected to MongoDB")
    return tweets

# Post a tweet


def post_tweet(tweets, client):
    tweet = tweets.find_one()
    if tweet:
        tweet_text = tweet['text']
        print(f"Posting tweet: {tweet_text}")
        try:
            response = client.create_tweet(text=tweet_text)
            print(response.data)
            tweet_id = response.data['id']
            user = client.get_me()
            user_name = user.data.username
            print(
                f"Posted tweet: https://twitter.com/{user_name}/status/{tweet_id}")
            tweets.delete_one({'_id': tweet['_id']})
            print(f"Posted tweet and removed from database")
        except Exception as e:
            print(f"Failed to post tweet: {e}")
    else:
        print("No tweets found in database")


def generate_random_tweet():
    tweets = [
        "This is a random tweet - did I make you smile?",
        "Hello there, Twitter!",
        "I'm Abby! How are you today!?",
        # Add as many tweets as you like
    ]

    return random.choice(tweets)


def post_random_tweet(tweets, client):
    tweet_text = generate_random_tweet()
    print(f"Posting random tweet: {tweet_text}")
    client.create_tweet(text=tweet_text)
    print(f"Posted random tweet")


# Schedule tweets


def schedule_tweets(tweets, client):
    print("Scheduling tweets...")
    scheduler = BackgroundScheduler()
    for tweet in tweets.find():
        scheduler.add_job(post_tweet, 'date',
                          run_date=tweet['run_date'], args=(tweets, client))
    print("Tweets scheduled")
    scheduler.start()


def schedule_random_tweets(tweets, client):
    print("Scheduling random tweets every hour...")
    scheduler = BackgroundScheduler()
    scheduler.add_job(post_random_tweet, 'interval',
                      hours=1, args=(tweets, client))
    print("Random tweets scheduled")
    scheduler.start()


def add_tweet_to_schedule(tweets, text, run_date):
    # Get the highest tweet id in the database
    last_tweet = tweets.find_one(sort=[('tweet_id', -1)])
    last_tweet_id = last_tweet['tweet_id'] if last_tweet else 0

    # Assign an id to the new tweet
    tweet_id = last_tweet_id + 1

    # Add the tweet to the database
    tweets.insert_one(
        {'tweet_id': tweet_id, 'text': text, 'run_date': run_date})
    print(f"Added tweet '{text}' to schedule at {run_date}")


# Tweet Commands


def list_scheduled_tweets(tweets):
    all_tweets = tweets.find()
    count = tweets.count_documents({})

    if count == 0:
        print("No scheduled tweets found.")
    else:
        print("Scheduled tweets:")
        for tweet in all_tweets:
            print(
                f"{tweet['tweet_id']}: {tweet['text']} at {tweet['run_date']}")


def delete_scheduled_tweet(tweets, tweet_id):
    # Convert the tweet id to an integer
    tweet_id = int(tweet_id)

    # Delete the tweet from the database
    result = tweets.delete_one({'tweet_id': tweet_id})

    if result.deleted_count == 1:
        print(f"Deleted scheduled tweet with ID {tweet_id}")
    else:
        print(f"No scheduled tweet found with ID {tweet_id}")


def main():
    client = connect_to_twitter()
    tweets = connect_to_mongodb()

    # Start the scheduler in a new thread
    scheduler_thread = threading.Thread(
        target=schedule_tweets, args=(tweets, client))
    scheduler_thread.start()

    random_scheduler_thread = threading.Thread(
        target=schedule_random_tweets, args=(tweets, client))
    random_scheduler_thread.start()

    # add_tweet_to_schedule(tweets, "Hello, Twitter!", '2023-07-10 10:00:00')
    list_scheduled_tweets(tweets)

    # The main thread is free to do other things
    while True:
        command = input("Enter a command: ")
        if command == 'list':
            list_scheduled_tweets(tweets)
        elif command.startswith('delete'):
            _, tweet_id = command.split()
            delete_scheduled_tweet(tweets, tweet_id)
        elif command.startswith('add'):
            tweet_text = input("What is your tweet?")
            tweet_date_str = input("When should it be posted?")
            tweet_date = dateparser.parse(tweet_date_str)

            if tweet_date is None:
                print("Sorry, I didn't understand that date. Please try again")
            else:
                add_tweet_to_schedule(tweets, tweet_text, tweet_date)
                schedule_tweets(tweets, client)
        elif command == 'exit':
            break


if __name__ == "__main__":
    main()
