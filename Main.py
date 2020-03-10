from bs4 import BeautifulSoup
from win10toast import ToastNotifier
from urllib.request import Request, urlopen
from requests_html import HTMLSession

def sendToast(message):
	toaster = ToastNotifier()
	toaster.show_toast("Sample Notification",message)

# def getTimeStamp(language = "EN"):
# 	bestdori_url = "http://bestdori.com"

# 	req = Request(bestdori_url, headers={'User-Agent': 'Mozilla/5.0'})
# 	webpage = urlopen(req).read()
# 	soup = BeautifulSoup(webpage, "lxml")
# 	print(soup.prettify())

def getTimeStamp(language ="EN"):
	bestdori_url = "http://bestdori.com"
	session  = HTMLSession()
	resp = session.get(bestdori_url)
	resp.html.render(sleep=2)
	print(resp.html.text)

	#soup = BeautifulSoup(resp.html.html, "lxml")
	#print(soup.prettify())
	# print()

if __name__ == "__main__":
	getTimeStamp()
	# sendToast("It worked!")
	# jsTest()