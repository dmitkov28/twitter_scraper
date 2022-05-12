import csv
import os

from twitter_api import get_tweets_for_user, get_user_id


#Example

user_id = get_user_id('xkcd')


data = get_tweets_for_user(user_id, '2022-02-01', '2022-05-11', user_name='Randall Munroe', user_profile_url='https://twitter.com/xkcd')


