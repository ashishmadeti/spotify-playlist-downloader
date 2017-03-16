import requests
import os
import string
import json
from bs4 import BeautifulSoup

def fetch(song, **kwargs):
    if kwargs['backend'] == 'lastfm':
        image = fetch_from_lastfm(song)
    elif kwargs['backend'] == 'google':
        image = fetch_from_google(song)
    return image

def fetch_from_google(song):
    ''' Downloads art from images.google.com '''

    query = song['artist'] + song['name'] + 'cover art google play' # Art work can be of huge size so the 'google play' in query mostly results into smaller images
    query = string.replace(query, ' ', '+')
    url = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1366&bih=649&q=%s&oq=%s&gs_l=img.3...857.12029.0.12205.36.14.1.20.21.0.301.1337.0j7j0j1.8.0....0...1ac.1.64.img..7.15.1346.0..0j0i24k1.22gw0wRgCfk'%(query, query)
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    tag = soup.find('div', {'class': 'rg_meta'})    #The first result
    dictionary = json.loads(tag.string)
    link = dictionary.get('ou', None)
    if link == None:
        print 'No link found'
        return
    image_download = link.decode('unicode-escape')
    #print 'Image download link is %s' %image_download
    try:
        image = requests.get(image_download).content
        return image
    except:
        print 'Could not download image'

def fetch_from_lastfm(song):
    ''' Downloads art from last.fm '''

    artist = song['artist']
    album = song['album']
    track = song['name']
    #Last.fm
    API_KEY = os.environ.get('LASTFM_API_KEY', None)
    if API_KEY == None:
        print 'You need to add an environment variable for LASTFM_API_KEY\n'
        return
    url = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=%s&artist=%s&album=%s&format=json'%(API_KEY,artist,album)
    response = requests.get(url).json()
    image_download = ''
    images = []
    try:
        images = response.get('album', None).get('image', None)
    except:
        print 'No images found for this album/track'
        return
    for image in reversed(images):
        if image.get('size') == 'extralarge':       #The most suitable image size
            image_download = image.get('#text')
            break
        elif image.get('size') == 'large':
            image_download = image.get('#text')
            break
        elif image.get('size') == 'medium':
            image_download = image.get('#text')
            break
        elif image.get('size') == 'small':
            image_download = image.get('#text')
            break
    if image_download == '':
        return
    try:
        image = requests.get(image_download).content
        return image
    except:
        print 'Could not download image'

