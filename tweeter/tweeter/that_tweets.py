__author__ = 'Hazel'
import tweepy
import json

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

def authenticate():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error!')

    auth.set_access_token(access_token,access_token_secret)

    api = tweepy.API(auth)
    print(api.me().name)

    response = api.update_status(status='Test tweet using Tweepy via OAuth!')

def load_credentials():
    global consumer_key, consumer_secret, access_token, access_token_secret

    with open('twitter_creds.json', mode='r', encoding='utf-8') as file:
        data = json.load(file)
        twitter_creds = data['twitter_creds']
        consumer_key = twitter_creds['consumer_key']
        consumer_secret = twitter_creds['consumer_secret']
        access_token = twitter_creds['access_token']
        access_token_secret = twitter_creds['access_token_secret']

load_credentials()
authenticate()