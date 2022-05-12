import os
import time

import dotenv
import requests

from helpers import convert_date

dotenv.load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
}


def is_within_rate_limit(response):
    remaining_requests = int(response.headers.get('x-rate-limit-remaining'))
    return remaining_requests > 0


def timeout(mins: int):
    print(f'Sleeping for {mins}...')
    time.sleep(mins * 60)


def get_user_id(username: str):
    url = f'https://api.twitter.com/2/users/by/username/{username}'
    resp = requests.get(url, headers=headers)

    if not is_within_rate_limit(resp):
        timeout(15)

    user_id = resp.json().get('data').get('id')
    return user_id


def get_rt_full_text(tweet_id):
    url = f'https://api.twitter.com/2/tweets/{tweet_id}'

    params = {
        'expansions': 'referenced_tweets.id'
    }

    resp = requests.get(url, headers=headers, params=params)

    if not is_within_rate_limit(resp):
        timeout(15)

    if resp.status_code == 200:
        tweet_full_text = resp.json().get('includes').get('tweets')[0].get('text')
    return tweet_full_text


def get_tweets_for_user(user_id: str, start_date: str, end_date: str, user_profile_url: str, user_name: str = None):
    data = []
    start_date_converted = convert_date(start_date)
    end_date_converted = convert_date(end_date)

    url = f'https://api.twitter.com/2/users/{user_id}/tweets'

    params = {
        'pagination_token': None,
        'start_time': start_date_converted,
        'end_time': end_date_converted,
        'tweet.fields': 'created_at',
    }

    resp = requests.get(url, headers=headers, params=params)

    if not is_within_rate_limit(resp):
        timeout(15)

    while True:
        if not resp.json().get('data'):
            break

        if resp.status_code != 200:
            print(resp.status_code)
            print(resp.text)
            break

        for item in resp.json().get('data'):
            tweet_id = item.get('id')
            tweet = item.get('text')

            if tweet.endswith('…'):
                tweet = get_rt_full_text(tweet_id)

            created_at = item.get('created_at')
            tweet_url = f'https://twitter.com/{user_id}/status/{tweet_id}'

            row = [
                user_name,
                user_profile_url,
                'active',
                created_at,
                tweet_url,
                tweet,
            ]

            data.append(row)
            print(row)

        pagination_token = resp.json().get('meta').get('next_token')
        params['pagination_token'] = pagination_token



        if not pagination_token:
            return data

        resp = requests.get(url, headers=headers, params=params)
