""" BandoriNotifier

Program that notifies how much time is left in a Bang Dream event.

Must have the following libaries installed before running: requests_html, 
	win10toast

Author: Noemi Valadez-Monarrez
"""

#from bs4 import BeautifulSoup
from win10toast import ToastNotifier
#from urllib.request import Request, urlopen
from requests_html import HTMLSession
import re, json, time

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

def sendToast(title: str, message: str) -> None:
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
	try: 
		toaster.show_toast(title, message, icon_path="bandori_star_ico.ico", duration=10, threaded=True)
	except AttributeError:
		# Exception is raised due to error in win10toast source code
		pass

def formatDivString(element_text: str) -> str:
	"""
	Determines what event deadline element_text describes and formats
		string 
	
	Args:
		element_text (str): Text
		
	Returns:
		message: Formatted message for specific event (with time
	"""
	
	# TODO: add regex to only obtain 
	
	# If the event is going to end
	if "Ends" in element_text:
		timestamp_pattern = r'Ends in ([a-zA-Z0-9 ]*)'
		matches = re.search(timestamp_pattern, element_text)
		return "Event ending in " + matches.group(1)
	
	# If the event is going to start
	elif "Starts" in element_text:
		timestamp_pattern = r'Starts in ([a-zA-Z0-9 ]*)'
		matches = re.search(timestamp_pattern, element_text)
		return "Event starting in " + matches.group(1)
	
	# If the event has not started and a date hasn't been determined
	elif "Not" in element_text:
		return "Event hast started and date not determined " + element_text
	

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

	# Search for specific HTML div elements in HTML code
	# Via Bestdori's HTML code, event info is stored under IDs
	#	".title.is-6" and ".subtitle.is-6"
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
	
	# Storing text from div containers into lists and
	#	 skipping elements we do not need
	for el in event_name_elements:
		if el.text not in skip_texts:
			event_titles.append(el.text)
	
	for el in timestamp_elements:
		if el.text not in skip_texts:
			timestamp_texts.append(el.text)

	
# 	for i in range(len(event_titles)):
# 		print("{} - {}".format(event_titles[i], timestamp_texts[i]))
# 
# 	print("___")
	
	
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
	# IDEA: Use formatDivString here for message that will be sent
	
	list_servers = servers
	#print(list_servers)
	timestamps_data = getTimeStampsData()
	#print(timestamps_data)
	for server in list_servers:
		#print(server)
		#print(timestamps_data[server])
		#print(timestamps_data[server][0])
		#print(timestamps_data[server][1])
		sendToast("{} event - {} ".format(server, timestamps_data[server][0]),  formatDivString(timestamps_data[server][1]))
		print("{} event - {} ".format(server, timestamps_data[server][0]),  formatDivString(timestamps_data[server][1]))
		time.sleep(60)
if __name__ == "__main__":
	# Runs when only Main.py is ran first
	# TODO: Make GUI that sets setting and runs Main.py
	
	# Obtain settings from settings.json
	settings = readSettings()
	
	
	# TODO: Add frequency settings to settings.json (e.g. how frequently 
	#	does the user want the toast to be sent)
	# Daily? Hourly? 4 times a day? Twice a day?
	# 24 = hourly (once every hour); 4 = 4 times a day; 2 = 2 times a day; 1 = 1 time a day
	
	# IDEA:
	# Ask the user: at what time do you want to be notified?
	# Then notify at that time and at each increment based on the frequency setting  
	interval = 60 * 60 	# 60 sec * 60 min
	while True:
		sendTimeStamp(settings["servers"])
		time.sleep(interval)
	# sendToast("It worked!")
	# jsTest()