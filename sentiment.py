import pandas as pd
import warnings
import tweepy
import re
from textblob import TextBlob
from dotenv import load_dotenv
import os
from boto.s3.connection import S3Connection
warnings.filterwarnings('ignore')


# credentials
load_dotenv()
#consumer_key = os.getenv('consumer_key')
#consumer_secret = os.getenv('consumer_secret')
#access_token = os.getenv('access_token')
#access_token_secret = os.getenv('access_token_secret')

# consumer_key = os.environ['consumer_key']
# consumer_secret = os.environ['consumer_secret']
# access_token = os.environ['access_token']
# access_token_secret = os.environ['access_token_secret']

#s3 = S3Connection(os.environ['consumer_key'], os.environ['consumer_secret'])
#s4 = S3Connection(os.environ['access_token'], os.environ['access_token_secret'])

consumer_key='Yi6HI4uawDXnC2LTEHLCdJTxr'
consumer_secret='adaz260pZR0o5S0dGRVYA1A1erFTQK0B4cp7PijOH6lPepbW1A'

access_token='1361341447237038080-iXzZQqgWZJwodmEytnu2yup8guAaNs'
access_token_secret='rNa5NAlKOHVsViio8XatUv28Old3pOl6DXBNVflBA0rJv'




# call API
try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
except Exception as e:
    print(e)
    print("\n SOMETHING WRONG WHILE CALLING API \n")

df = pd.DataFrame(columns=['Tweets', 'Created_at', 'Name', 'Location', 'Verified',
                           'Followers_count', 'Statuses_count', 'Retweet_count'])


def stream(query, num):
    if df.shape[0] > 0:
        df.drop(df.index, inplace=True)

    i = 1
    for tweet in tweepy.Cursor(api.search, q=query, lang='en', exclude='retweets', result_type='recent',
                               tweet_mode='extended').items(num):

        print(i, end='\r')

        df.loc[i, 'Tweets'] = tweet.full_text
        df.loc[i, 'Created_at'] = tweet.user.created_at
        df.loc[i, 'Name'] = tweet.user.name
        df.loc[i, 'Location'] = tweet.user.location
        df.loc[i, 'Verified'] = tweet.user.verified
        df.loc[i, 'Followers_count'] = tweet.user.followers_count
        df.loc[i, 'Statuses_count'] = tweet.user.statuses_count
        df.loc[i, 'Retweet_count'] = tweet.retweet_count

        i += 1
        if i == 999:
            break
        else:
            pass

    return df


def clean_tweet(tweet):
    return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)',' ', tweet).split())


def analyse_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return "POSITIVE"
    elif analysis.sentiment.polarity < 0:
        return "NEGATIVE"
    else:
        return "NEUTRAL"


def score(tweet):
    analysis = TextBlob(tweet)
    return round(analysis.sentiment.polarity, 2)

