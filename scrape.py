import config
import redis
import sys
import search_terms
import random
import cleaners
import db
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome(executable_path=config.path_to_chromedriver)
start_date = 1880
end_date = 1950

def no_entries_found():
	try: 
		browser.find_element_by_xpath("/html/body/div[1]/table/tbody/tr[3]/td[2]/div[1]/h2")
		return True
	except NoSuchElementException:
		return False

def one_result_found():
	try:
		r = browser.find_element_by_xpath("/html/body/div[6]/div/i[4]").get_attribute("innerText")
		if r[:8] == "1 result":
			return True
	except NoSuchElementException:
		return False

def scrape():
	"""scrape record"""
	photo_id = browser.find_element_by_xpath("//*[@id=\"record-info\"]/table/tbody/tr/td/table/tbody/tr[1]/td[2]").text
	
	"""check our db to see if we've scraped this photo before"""
	if not database.check_record(session, photo_id):
	
		"""find title"""
		data = browser.find_elements_by_css_selector(".bibInfoData")
		title = data[3].text
		
		"""finding date is a little trickier, because they put it different places"""
		date = data[5].text
		cleaner_date = cleaners.clean_date(date)
		
		"""is this actually a date? let's find out!"""
		date_found = False
		while not date_found:
			if cleaner_date.startswith("19") or cleaner_date.startswith("18"):
				date_found = True
			else:
				date = data[4].text
				cleaner_date = cleaners.clean_date(date)

		"""scrape the rest of our record"""
		entry_url = browser.find_element_by_name("LinkURL").get_attribute("value")
		image_url = browser.find_element_by_css_selector("#image-link > table > tbody > tr:nth-child(2) > td > a").get_attribute("href")
		short_url = cleaners.clean_url(entry_url)
		cleaner_title = cleaners.clean_title(title)

		"""load our record into a dict"""
		record = {
			"photo_id": str(photo_id),
			"title": str(cleaner_title),
			"date": str(cleaner_date),
			"entry_url": str(short_url),
			"image_url": str(image_url),
				}

		"""add our record to the heroku postgres db"""
		database.add_record(session, record)
		return True
				
	else:
		print "Duplicate found..."
		return False

def start_digging():
	count = 0
	while count < 21:
		for term in search_terms.list:

			clean_term = term.replace(" ", "+") 
			rand_date = str(random.randrange(start_date, end_date, 3))
			url = "http://sflib1.sfpl.org:82/search/X?SEARCH=\"%s\"&x=0&y=0&m=&p=&Da=1880&Db=%s&SORT=D" % (clean_term, rand_date)
			
			browser.get(url)
			browser.implicitly_wait(10)

			if not no_entries_found() and not one_result_found():
				"""if we've got more than 1 entry, click on View Full Record"""
				browser.find_element_by_link_text("View Full Record").click()
				if scrape():
					count += 1

			elif one_result_found():
				if scrape():
					count += 1

			elif no_entries_found():
				print "No entries found..."

"""open our heroku postgres session"""
database = db.heroku()
session = database.make_session()

start_digging()

session.close()


