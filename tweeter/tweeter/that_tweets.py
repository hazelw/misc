__author__ = 'Hazel'
import requests

#CONSUMER_KEY = xxxxx

def generate_tweet():
    payload = {'status': 'test tweet from a python app :)'}
    response = requests.post("https://api.twitter.com/1.1/statuses/update.json", params=payload)

    if response.status_code != 200:
        print("Something went wrong!")
        print(response.text);
    else:
        print("Success!")
