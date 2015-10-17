import config
import requests
from twython import Twython
from selenium import webdriver
from PIL import Image
from StringIO import StringIO
import random
import os
import redis
import db
import cleaners

twitter = Twython(config.consumer_key, config.consumer_secret_key, config.access_token, config.access_token_secret)
redis_server = redis.Redis(host=config.redis_url, port=9392, password=config.redis_auth)

def already_tweeted(photo_id):

	"""ask redis if this photo_id has already been tweeted"""
	if redis_server.sismember("oldgoldmtn_record", photo_id):
		return True
	else:
		return False

def tweet_photo(record):

	"""first we parse our record"""
	record_string = str(record)
	record_list = record_string.split(", ")
	photo_id = record_list[1]
	title = record_list[2]
	date = record_list[3]
	entry_url = record_list[4]
	image_url = record_list[5]
	
	"""then we make our caption"""
	caption = cleaners.caption_maker(title, date, entry_url)

	"""then we grab our image and save it"""
	r = requests.get(image_url)
	image = Image.open(StringIO(r.content))
	photo_path = "./tmp/img/%s.jpg" % photo_id
	image.save(photo_path, format="JPEG")
	
	"""then we tweet our photo and caption"""
	picture = open(photo_path, "rb")
	r2 = twitter.upload_media(media=picture)
	twitter.update_status(status=caption, media_ids=[r2["media_id"]])

if __name__ == "__main__":

	"""make our temp img directory if doesn't exist already"""
	if not os.path.isdir("./tmp/img"):
		try:
			os.makedirs("./tmp/img")
		except OSError:
			if not os.path.isdir(path):
				raise

	"""open our database connection"""
	database = db.heroku()
	session = database.make_session()
	untweeted = True

	while untweeted:
		"""grab a random record"""
		rand_record = database.get_rand_record(session)

		"""check if we've tweeted this record before"""
		if not already_tweeted(rand_record.photo_id):
			redis_server.sadd("oldgoldmtn_record", rand_record.photo_id)
			tweet_photo(rand_record)
			untweeted = False
			print "Success!"

		else:
			print "Already tweeted! Re-randomizing."

	session.close()



