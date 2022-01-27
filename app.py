from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

app = Flask(__name__)


def get_page_urls(url):
    page_urls = [url]
    html_text = requests.get(url).text
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

def get_video_urls(homepage_url):
    episode_urls = get_episode_urls(get_page_urls(homepage_url))
    video_urls = OrderedDict()
    for url in episode_urls:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        for div in soup.find_all('div', class_="single-post-video"):
            for link in div.find_all('iframe'):
                video_urls[soup.title.string] = link.get('src')

    return video_urls


@app.route("/")
def index():
    url1 = 'https://anupamawatch.com/shark-tank-india/'
    url2 = 'https://molkkiserial.com/shark-tank-india/'
    url3 = 'https://herogayab.net/shark-tank-india/'
    return render_template("index.html", 
        data1 = get_video_urls(url1), 
        data2 = get_video_urls(url2),
        data3 = get_video_urls(url3))


if __name__ == "__main__":
    app.run()