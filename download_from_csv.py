'''
Script to download your spotify playlists:

Convert your spotify playlist to csv from here: http://joellehman.com/playlist
or provide playlist URI, your username and authorization token here
and then download all the songs through this script
Depends upon youtube_dl, eyed3 and unidecode pip packages
'''

from __future__ import unicode_literals
import os
import csv
import argparse
import json
import UserString

import eyed3
import youtube_dl
from unidecode import unidecode
import requests
import wget
from bs4 import BeautifulSoup


# Youtube-dl options
opts = {
    'format': 'bestaudio/best',
    'forcejson': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '256',
    }],
    'progress_hooks': '',
    'logger': '',
    'outtmpl': ''
}
# user-agents
headers = {
    'User-Agent' : 'Mozilla/5.0'
}


class MyLogger(object):

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def download_finish(d):
    if d['status'] == 'finished':
        print '\x1b[1A\x1b[2K'
        print "\x1b[1A[\033[93mConverting\033[00m] %s" % d['filename']

def download_image(keywords):
    keywords2 = '+'.join(keywords.split(' '))
    url = 'https://www.google.co.in/search?q=%s\&tbm=isch'%keywords2
    response = requests.get(url, headers = headers)
    htm = response.text
    soup = BeautifulSoup(htm, 'html.parser')
    imageURL = soup.find('img').get('src')
    wget.download(imageURL, out=keywords) # saves image as name "images"

def generate_csv(URI, username, auth_token):
    cmd = 'curl -X GET "https://api.spotify.com/v1/users/' + username + '/playlists/' + URI + '/tracks" -H "Accept: application/json" -H "Authorization: Bearer ' + auth_token + '"'
    os.system(cmd + ' > data.json')
    data = open('data.json', 'r+').read()
    data = json.loads(data)
    csv_data = UserString.MutableString()
    for track in xrange(len(data['items'])):
        name = data['items'][track]['track']['name']
        artist = data['items'][track]['track']['artists'][0]['name']
        album = data['items'][track]['track']['album']['name']
        date = data['items'][track]['added_at']
        csv_data.append(', '.join([name, artist, album, date]) + '\n')
    csv_data = str(csv_data)
    try:
        f = open('playlist.csv', 'w+')
        f.write(csv_data)
        f.close()
    except Exception as e:
        # print e
        raise Exception("Couldn't write csv file to disk")
    return 'playlist.csv'

# Command line parser arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--folder', default=os.getcwd(), 
        help="keep the files in the folder specified")
parser.add_argument('-c', '--create', 
        help="try to create folder if doesn't exist", action="store_true")
parser.add_argument('--skip', 
        help="number of songs to skip from the start of csv", type=int)
parser.add_argument('-s', '--search', nargs='*', 
        help="search source for songs, default is youtube")
parser.add_argument('-p', '--playlist', 
        help="Enter the playlist URI, with this you'd need username and token")
parser.add_argument('-u', '--username', help="Enter your username")
parser.add_argument('-t', '--token', 
        help="Enter authorization token, get it here:\
            https://developer.spotify.com/web-api/console/get-playlist-tracks/")
parser.add_argument('-i', '--csv', help="input a csv file")
args = parser.parse_args()

csvfile = None
if args.csv:
    if os.path.isfile(args.csv):
        csvfile = args.csv
    else:
        print 'No such csv file. Aborting..'
        exit()
elif args.playlist:
    username = None
    token = None
    if args.username:
        username = args.username
    else:
        username = raw_input("\033[93mEnter username to access api: \033[0m")
    if args.token:
        token = args.token
    else:
        token = raw_input(
        "if you don't have one, get it here: \033[94mhttps://developer.spotify.com/web-api/console/get-playlist-tracks/\n\033[93mEnter fresh token to access api: \033[0m"
        )
    csvfile = generate_csv(args.playlist, username, token)
else:
    parser.error("No action requested, add -p or -i. Or add -h for help")


folder = '' # will be set to current if it's not given in arguments
if args.folder:
    args.folder = os.path.relpath(args.folder)
    if os.path.isdir(args.folder):
        folder = os.path.relpath(args.folder)
        folder = args.folder
    elif args.create:
        try:
            os.makedirs(args.folder)
            folder = os.path.relpath(args.folder)
            folder = args.folder
        except e:
            print 'Error while creating folder'
            raise
    else:
        print 'No such folder. Aborting..'
        exit()
    print 'Storing files in', folder



songs = []
with open(csvfile, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the first line
    if args.skip:
        print 'Skipping', args.skip, 'songs'
        for i in range(args.skip):
            next(reader)
    for row in reader:
        songs.append({
            'name': unidecode(unicode(row[0], "utf-8")).strip(),
            'artist': unidecode(unicode(row[1], "utf-8")).strip(),
            'album': unidecode(unicode(row[2], "utf-8")).strip()
        })
for song in songs:
    probable_filename = folder + '/' + song['name'] + ' - ' + \
        song['artist'] + '.mp3'
    if os.path.isfile(probable_filename):
        # The file may already be there, so skip
        print '[\033[93mSkipping\033[00m] %s by %s' % \
            (song['name'], song['artist'])
        continue
    opts['progress_hooks'] = [download_finish]
    opts['logger'] = MyLogger()
    opts['outtmpl'] = folder + '/' + song['name'] + ' - ' + song['artist'] + '.%(ext)s'
    url = ' '.join([song['name'], song['artist']])
    if args.search:
        url = song['name'] + ' ' + song['artist'] + ' ' + args.search
        url = 'gvsearch1: ' + url
    else:
        url = 'ytsearch: ' + url
    print '[\033[91mFetching\033[00m] %s' % probable_filename
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([url])
    if os.path.isfile(probable_filename):
        afile = eyed3.load(probable_filename)
        afile.tag.title = unicode(song['name'], "utf-8")
        afile.tag.artist = unicode(song['artist'], "utf-8")
        afile.tag.album = unicode(song['album'], "utf-8")
        keywords = song['name'] + ' ' + song['artist']
        download_image(keywords)
        imagedata = open(keywords, 'rb').read()
        os.system("rm \"%s\"" %keywords)
        afile.tag.images.set(3, imagedata, 'image/jpeg', keywords)
        afile.tag.save()
    else:
        print '\x1b[1A\x1b[2K'
        print '\x1b[1A[\033[91mMetadata\033[00m] Could not set metadata for %s\nTemp' %  probable_filename

    print '\x1b[1A\x1b[2K'
    print '\x1b[1A[\033[92mDownloaded]\033[00m', song['name'], '-', song['artist']

