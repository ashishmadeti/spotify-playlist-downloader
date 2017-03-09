'''Script to download your spotify playlists

Convert your spotify playlists to csv from here: http://joellehman.com/playlist/
and then download all the songs through this script
Depends upon youtube_dl, eyed3 and unidecode pip packages
'''

from __future__ import unicode_literals
import os
import csv
import eyed3
import argparse
import youtube_dl
import json
from unidecode import unidecode
from urllib import urlopen, urlretrieve

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--folder', help="keep the files in the folder specified")
parser.add_argument('-c', '--create', help="try to create folder if doesn't exist",
                    action="store_true")
parser.add_argument('--skip', help="number of songs to skip from the start of csv",
                    type=int)
parser.add_argument('-q', '--query', help="enter the search query", type=str)
parser.add_argument('csv', help="input csv file")
args = parser.parse_args()

folder = ''
if os.path.isfile(args.csv):
    csvfile = args.csv
else:
    print 'No such csv file. Aborting..'
    exit()

if args.folder:
    if os.path.isdir(args.folder):
        folder = os.path.abspath(args.folder)
    elif args.create:
        try:
            os.makedirs(args.folder)
            folder = os.path.abspath(args.folder)
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

def download_album_art(song):
    ''' Here we download art for the said album/track '''

    artist = song['artist']
    album = song['album']
    track = song['name']
    #Last.fm
    API_KEY = '03f624c25bd2ffdbad319226716efe66'
    url = urlopen('http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=%s&artist=%s&album=%s&format=json'%(API_KEY,artist,album)).read()
    result = json.loads(url)
    images = []
    image_download = ''
    try:
        images = result.get('album', None).get('image', None)
    except:
        print 'No images found for this album/track'
        return

    for image in reversed(images):
        if image.get('size') != "":
            image_download = image.get('#text')
            break

    if image_download == '':
        return

    image_path = folder + '/' + track + ' - ' + artist + '.png'
    try:
        urlretrieve(image_download, image_path)
    except:
        print 'Could not download image'

for song in songs:
    probable_filename = folder + '/' + song['name'] + ' - ' + \
        song['artist'] + '.mp3'
    if os.path.isfile(probable_filename):
        # The file may already be there, so skip
        print '[\033[93mSkipping\033[00m] %s by %s' % \
            (song['name'], song['artist'])
        continue
    opts = {
        'format': 'bestaudio/best',
        'forcejson': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '256',
        }],
        'progress_hooks': [download_finish],
        'logger': MyLogger(),
        'outtmpl': folder + '/' + song['name'] + ' - ' + song['artist'] + '.%(ext)s'
    }
    if args.query == None:
        url = ' '.join([song['name'], song['artist'], 'audio', 'youtube'])
    else:
        url = ' '.join([song['name'], song['artist']]) + ' '
        url += args.query
    url = 'gvsearch1:' + url
    print '[\033[91mFetching\033[00m] %s' % probable_filename
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([url])

    download_album_art(song)

    if os.path.isfile(probable_filename):
        afile = eyed3.load(probable_filename)
        afile.tag.title = unicode(song['name'], "utf-8")
        afile.tag.artist = unicode(song['artist'], "utf-8")
        afile.tag.album = unicode(song['album'], "utf-8")
        try:
            image_path = folder + '/' + song['name'] + ' - ' + song['artist'] + '.png'
            art = open(image_path, 'rb').read()
            afile.tag.images.set(3, art, 'image/png', song['name'] + ' - ' + song['artist'])
        except:
            pass

        afile.tag.save()
    else:
        print '\x1b[1A\x1b[2K'
        print '\x1b[1A[\033[91mMetadata\033[00m] Could not set metadata for %s\nTemp' % \
            probable_filename

    print '\x1b[1A\x1b[2K'
    print '\x1b[1A[\033[92mDownloaded]\033[00m', song['name'], '-', song['artist']
