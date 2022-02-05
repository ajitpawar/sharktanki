from flask import Flask, render_template
import requests
import os
from bs4 import BeautifulSoup
from collections import OrderedDict
from models import setup_db, Movie, db_drop_and_create_all
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
setup_db(app)
# db_drop_and_create_all()  # drop and re-create table

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

                ## insert into DB
                entry = Movie(soup.title.string, link.get('src'), homepage_url)
                db.session.add(entry)

    db.session.commit()
    return

def insert_into_db(src):
    entry = Movie('test1', 'exmaple.com', src)
    db.session.add(entry)
    db.session.commit()

def index():
    urls = [
        'https://herogayab.net/shark-tank-india/',
        'https://anupamawatch.com/shark-tank-india/',
        'https://molkkiserial.com/shark-tank-india/'
    ]

    for url in urls:
        get_video_urls(url)


if __name__ == "__main__":
    # index()
    test()
    