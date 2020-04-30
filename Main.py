""" BandoriNotifier

Program that notifies how much time is left in a Bang Dream event.

Must have the following libaries installed before running: requests_html, 
	win10toast

Author: Noemi Valadez-Monarrez
"""

from bs4 import BeautifulSoup
from win10toast import ToastNotifier
from urllib.request import Request, urlopen
from requests_html import HTMLSession
import re
import json

def readSettings(filename = "settings.json") -> dict:
	"""
	Gets settings from json file and returns it as a dict.
	
	Args:
		filename (str): Name of json file for settings. Defautls to "settings.json"
		
	Returns:
		settings_dict (dict): Dict containing settings in a "setting_name: value" format
		
	"""
	settings_file = open(filename)
	settings_dict = json.load(settings_file)
	return settings_dict

def sendToast(message: str) -> None:
	"""
	Sends a Windows Toast notification with a defined message
	
	Args:
		message (str): Message to be sent in the toast notification
		
	Returns:
		None
	
	"""
	# IDEA: Toast should include all servers?

	# Creates a ToastNotifier object and send message 
	toaster = ToastNotifier()
	toaster.show_toast("Sample Notification",message)


def getTimeStampsData() -> dict:
	"""
	Obtains HTML code from bandori.com and scrapes time data
		for requested events	
		
	Args: 
		None
		
	Returns:
		timestamps_dict (dict): Dictionary containing servers and their current event data
	"""

	# Open request to bestdori.com and store html content
	bestdori_url = "http://bestdori.com"
	session  = HTMLSession()
	resp = session.get(bestdori_url)
	
	# sleep = 2 works to render dynamic content before obtaining
	#	HTML code
	resp.html.render(sleep=2)

	# Search for HTML div IDs in HTML code
	event_name_elements = resp.html.find(".title.is-5")
	timestamp_elements = resp.html.find(".subtitle.is-6")

	# Items in the following lists are grouped by their index number
	# EG: event_titles[2] is the title for the event that corresponds
	#	to the timestamp in timestamp_texts[2]
	event_titles = []
	timestamp_texts = []

	# HTML text to be skipped 
	skip_texts = {"Bestdori! - The Ultimate BanG Dream GBP Resource Site", 
				"News", "Support Us", "Support Bestdori!"}

	# Storing text from div containers into lists
	for el in event_name_elements:
		if el.text not in skip_texts:
			event_titles.append(el.text)
	
	for el in timestamp_elements:
		if el.text not in skip_texts:
			timestamp_texts.append(el.text)

	
	for i in range(len(event_titles)):
		print("{} - {}".format(event_titles[i], timestamp_texts[i]))

	print("___")
	
	
	# Dict is in the format of {server, (event_title, timestamp_text)}
	# EX: {'EN': ('Backstage Pass 2', 'Ends in 3 days 22 hrs 8 min 26 sec'}
	timestamps_dict = dict()

	# Creating dict for easier lookup
	for i in range(len(event_titles)):
		
		# Matches for: [text] ([server])
		# EG: Ends in 3 days 22 hrs 8 min 26 sec (EN)
		re_pattern = r'([a-zA-Z\s\d]+)\(([A-Z]{2})\)'
		matches = re.search(re_pattern, timestamp_texts[i])
		timestamps_dict[matches.group(2)] = (event_titles[i], matches.group(1).strip())

	return timestamps_dict

def sendTimeStamp(servers: list) -> None: 
	
	list_servers = servers
	timestamps_data = getTimeStampsData()


if __name__ == "__main__":
	# At what frequency did you want to send the toast?
	
	# Obtain settings from settings.json
	settings = readSettings()
	# TODO: Add frequency settings to settings.json (e.g. how frequently 
	#	does the user want the toast to be sent)
	
	sendTimeStamp(settings["servers"])
	# sendToast("It worked!")
	# jsTest()