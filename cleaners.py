import config
import requests
import json
import re
import os

def clean_title(title):
	cleanup = {"]":"", "[":"", ".":"", "graphic":""}
	for i, j in cleanup.iteritems():
		title = title.replace(i, j)
	return title.rstrip()

def clean_date(date):
	if date == "[n.d.]":
		return "undated"
	else:
		date = re.sub("\D", "", date)
		date = date[0:4]
		return date

def clean_url(long_url):
	google = "https://www.googleapis.com/urlshortener/v1/url?key=" + config.short_url_key
	payload = {"longUrl": long_url}
	headers = {"Content-Type": "application/json"}
	r = requests.post(google, data=json.dumps(payload), headers=headers)
	json_obj = json.loads(r.content)
	short_url = json_obj["id"]
	return short_url

def caption_maker(title, date, entry_url):
	caption = title + ", " + date + " " + entry_url
	while len(caption) > 140:
		title = title.rsplit(" ", 1)[0]
		caption = title + "..." + ", " + date + " | " + entry_url
	return caption