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
from unidecode import unidecode
import requests
import wget
from bs4 import BeautifulSoup


# Globals go here

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


# Command line parser arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--folder', default=os.getcwd(), help="keep the files in the folder specified")
parser.add_argument('-c', '--create', help="try to create folder if doesn't exist", action="store_true")
parser.add_argument('--skip', help="number of songs to skip from the start of csv", type=int)
parser.add_argument('-s', '--search', nargs='*', help="search these keywords and download it(First result as mp3)")
parser.add_argument('-i', '--csv', help="input a csv file")
args = parser.parse_args()


# If no option was specified, throw error
if not (args.csv or args.search):
    parser.error("No action requested, add -s or -i. Or add -h for help")

csvfile = None
if args.csv:
    if os.path.isfile(args.csv):
        csvfile = args.csv
    else:
        print 'No such csv file. Aborting..'
        exit()

folder = '' # will be set to current if it's not given in arguments
if args.folder:
    args.folder = os.path.relpath(args.folder)
    print "folder: ", args.folder
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



# This section executes only if a csv file is passed
def download_from_csv():
    global folder, csvfile
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
        url = ' '.join([song['name'], song['artist'], 'audio', 'youtube'])
        url = 'ytsearch:' + url
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

def download_through_search_terms():
    global folder
    keywords = (' '.join(args.search) if type(args.search)==list else args.search)
    probable_filename = folder + '/' + keywords + '.mp3'
    if os.path.isfile(probable_filename):
        # This file is already there, so skip
        print '[\033[93mSkipping\033[00m] %s'%(probable_filename)
        return
    opts['progress_hooks'] = [download_finish]
    opts['logger'] = MyLogger()
    opts['outtmpl'] = probable_filename
    url = 'ytsearch:' + keywords
    print '[\033[91mFetching\033[00m] %s' %probable_filename
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([url])
    if os.path.isfile(probable_filename):
        afile = eyed3.load(probable_filename)
        print os.listdir('.')
        print probable_filename
				#afile.tag.title = unicode(keywords, "utf-8")
				#afile.tag.artist = unicode(song['artist'], "utf-8")
				#afile.tag.album = unicode(song['album'], "utf-8")
        afile.tag.title = keywords
        download_image(keywords)
        imagedata = open(keywords, 'rb').read()
        os.system('rm ' + keywords)
        afile.tag.images.set(3, imagedata, 'image/jpeg', keywords)
        afile.tag.save()
    else:
        print '\x1b[1A\x1b[2K'
        print '\x1b[1A[\033[91mMetadata\033[00m] Could not set metadata for %s\nTemp' % probable_filename
    print '\x1b[1A\x1b[2K'
    print '\x1b[1A[\033[92mDownloaded]\033[00m', probable_filename


if args.search:
    download_through_search_terms()
if args.csv:
    download_from_csv()
