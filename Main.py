from bs4 import BeautifulSoup
from win10toast import ToastNotifier
from urllib.request import Request, urlopen
from requests_html import HTMLSession

def sendToast(message):
	toaster = ToastNotifier()
	toaster.show_toast("Sample Notification",message)


def getTimeStamp(language ="EN"):
	bestdori_url = "http://bestdori.com"
	session  = HTMLSession()
	resp = session.get(bestdori_url)
	resp.html.render(sleep=2)

	event_name_elements = resp.html.find(".title.is-5")
	timestamp_elements = resp.html.find(".subtitle.is-6")

	event_titles = []
	timestamp_texts = []

	skip_texts = {"Bestdori! - The Ultimate BanG Dream GBP Resource Site", "News", "Support Us", "Support Bestdori!"}

	for el in event_name_elements:
		if el.text not in skip_texts:
			event_titles.append(el.text)
	print("____")
	for el in timestamp_elements:
		if el.text not in skip_texts:
			timestamp_texts.append(el.text)

	for i in range(len(event_titles)):
		print("{} - {}".format(event_titles[i], timestamp_texts[i]))

if __name__ == "__main__":
	getTimeStamp()
	# sendToast("It worked!")
	# jsTest()