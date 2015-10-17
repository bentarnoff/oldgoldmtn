import os
from selenium import webdriver

consumer_key = os.environ.get("OLDGOLDMTN_CONSUMER_KEY")
consumer_secret_key = os.environ.get("OLDGOLDMTN_CONSUMER_SECRET")
access_token = os.environ.get("OLDGOLDMTN_ACCESS_TOKEN")
access_token_secret = os.environ.get("OLDGOLDMTN_ACCESS_TOKEN_SECRET")

short_url_key = os.environ.get("URL_SHORT_CONSUMER_KEY")

path_to_chromedriver = "/Users/ben/chromedriver/chromedriver"

redis_url = os.environ.get("REDIS_TOGO_URL")
redis_auth = os.environ.get("REDIS_TOGO_AUTH")

heroku_url = os.environ.get("HEROKU_POSTGRES_URL")