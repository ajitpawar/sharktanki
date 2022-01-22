import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

homepage_url = 'https://anupamawatch.com/shark-tank-india/'

def get_page_urls():
	page_urls = [homepage_url]
	html_text = requests.get(homepage_url).text
	soup = BeautifulSoup(html_text, 'html.parser')
	for link in soup.find_all('a', class_="page"):
	    page_urls.append(link.get('href'))

	return page_urls

def get_episode_urls(page_urls):
	episode_urls = []
	for url in page_urls:
		html_text = requests.get(url).text
		soup = BeautifulSoup(html_text, 'html.parser')
		for h2 in soup.find_all('h2', class_="post-box-title"):
			for link in h2.find_all('a'):
				episode_urls.append(link.get('href'))

	return episode_urls

def get_video_urls(episode_urls):
	video_urls = OrderedDict()
	for url in episode_urls:
		html_text = requests.get(url).text
		soup = BeautifulSoup(html_text, 'html.parser')
		for div in soup.find_all('div', class_="single-post-video"):
			for link in div.find_all('iframe'):
				video_urls[soup.title.string] = link.get('src')

	return video_urls


# Main
page_urls = get_page_urls()
episode_urls = get_episode_urls(page_urls)
video_urls = get_video_urls(episode_urls)
print video_urls
