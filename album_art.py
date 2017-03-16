import requests
import os
import json
from bs4 import BeautifulSoup


def fetch(song, **kwargs):
    if kwargs.get('backend', None) == 'lastfm':
        image = fetch_from_lastfm(song)
        if image:
            print 'Downloaded image from Lastfm'
    else:
        image = fetch_from_google(song)
        if image:
            print 'Downloaded image from Google'
    return image


def fetch_from_google(song):
    ''' Downloads art from images.google.com '''

    query = '+'.join([song['name'], song['artist'], 'cover', 'art'])
    url = 'https://www.google.co.in/search?tbm=isch&q=%s' % query
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    tag = soup.find('div', {'class': 'rg_meta'})  # The first result
    try:
        dictionary = json.loads(tag.string)
    except AttributeError, e:
        print e
        return
    image_download_link = dictionary.get('ou', None)
    try:
        image_download_link = image_download_link.decode('unicode-escape')
        image = download_image_from_link(image_download_link)
    except:
        print 'No link found'
    return image


def fetch_from_lastfm(song):
    ''' Downloads art from last.fm '''

    artist = song['artist']
    album = song['album']
    API_KEY = os.environ.get('LASTFM_API_KEY', None)
    if API_KEY is None:
        print 'You need to add an environment variable for LASTFM_API_KEY'
        return
    url = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=%s&artist=%s&album=%s&format=json' % (API_KEY, artist, album)
    response = requests.get(url).json()
    album_dict = response.get('album', None)
    try:
        images = album_dict.get('image', None)
    except:
        print 'No images found for this album/track'
        return
    for image in reversed(images):
        current_size = image.get('size')
        if current_size != 'mega' and current_size != '':   # There is also a size with value "" in the response JSON
            image_download_link = image.get('#text', None)
            break
    try:
        image = download_image_from_link(image_download_link)
    except:
        print 'No link found'
    return image


def download_image_from_link(url):
    try:
        image = requests.get(url).content
        return image
    except:
        print 'Could not download image'
