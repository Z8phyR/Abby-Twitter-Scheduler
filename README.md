# Abby Twitter Scheduler

Abby Twitter Scheduler is a Python script that allows you to schedule and post tweets to Twitter using the Tweepy library and MongoDB for storage.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.x installed
- Tweepy library installed (`pip install tweepy`)
- dotenv library installed (`pip install python-dotenv`)
- MongoDB installed and running
- Twitter API credentials (API key, API secret key, Access token, and Access token secret)
- MongoDB connection details (URI and database name)

## Installation

1. Clone this repository to your local machine or download the script file directly.

2. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and provide the following environment variables:

   ```
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
   MONGO_URI=your_mongodb_uri
   MONGO_DB_NAME=your_mongodb_database_name
   ```

4. Customize the script to fit your needs:
   - Modify the `generate_random_tweet` function to include your desired set of random tweets.
   - Adjust the scheduling logic in the `schedule_tweets` and `schedule_random_tweets` functions as required.

## Usage

1. Run the script using the following command:

   ```
   python main.py
   ```

2. Follow the prompts to interact with the script:

   - Use `list` to list all scheduled tweets.
   - Use `delete <tweet_id>` to delete a scheduled tweet by its ID.
   - Use `add` to add a new tweet to the schedule.

3. The script will automatically schedule and post tweets based on the provided schedule and random intervals.

## License

This project is licensed under the [MIT License](LICENSE).
