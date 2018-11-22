#!/usr/bin/env python
from __future__ import unicode_literals
import os
import csv
import eyed3
import argparse
import youtube_dl
import spotipy
import spotipy.util as util
from unidecode import unidecode


def get_songs_from_csvfile(csvfile, args):
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
    return songs


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


def download_songs(songs, folder):
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
     #       'verbose': True,
            'progress_hooks': [download_finish],
            'logger': MyLogger(),
            'outtmpl': folder + '/' + song['name'] + ' - ' + song['artist'] + '.%(ext)s'
        }
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
            afile.tag.save()
        else:
            print '\x1b[1A\x1b[2K'
            print '\x1b[1A[\033[91mMetadata\033[00m] Could not set metadata for %s\nTemp' % \
                probable_filename

        print '\x1b[1A\x1b[2K'
        print '\x1b[1A[\033[92mDownloaded]\033[00m', song['name'], '-', song['artist']


def get_songs_from_playlist(tracks, args):
    songs = []
    for item in tracks['items'][args.skip:]:
        track = item['track']
        songs.append({
            'name': unidecode(track['name']).strip(),
            'artist': unidecode(track['artists'][0]['name']).strip(),
            'album': unidecode(track['album']['name']).strip()
        })
    return songs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', help="keep the files in the folder specified")
    parser.add_argument('-c', '--create', help="try to create folder if doesn't exist",
                        action="store_true")
    parser.add_argument('--skip', help="number of songs to skip from the start of csv",
                        type=int)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-csv', help="input csv file")
    group.add_argument('-username', help="username of your spotify account")

    args = parser.parse_args()

    # getting current working directory
    folder = os.path.dirname(os.path.realpath(__file__))

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
    if args.csv:
        if os.path.isfile(args.csv):
            csvfile = args.csv
            songs = get_songs_from_csvfile(csvfile, args)
            download_songs(songs, folder)
        else:
            print 'No such csv file. Aborting..'
            exit()

    if args.username:
        scope = 'playlist-read playlist-read-private'
        token = util.prompt_for_user_token(args.username, scope)
        if token:
            sp = spotipy.Spotify(auth=token)
            try:
                playlists = sp.user_playlists(args.username)
            except spotipy.client.SpotifyException:
                print "Invalid Username"
                exit()
            if len(playlists) > 0:
                print "All Playlists: "
                for index, playlist in enumerate(playlists['items']):
                    print str(index + 1) + ": " + playlist['name']
                n = raw_input("Enter S.N. of playlists (seprated by comma): ").split(",")
                if n:
                    for i in xrange(0, len(n), 2):
                       playlist_folder = folder+"/"+playlists['items'][int(n[i]) - 1]['name']
                       print 'Storing files in', playlist_folder
                       if not os.path.isdir(playlist_folder):
                            try:
                                os.makedirs(playlist_folder )
                            except e:
                                print 'Error while creating folder'
                                raise
                       playlist_id = playlists['items'][int(n[i]) - 1]['id']
                       tracks = sp.user_playlist(args.username, playlist_id,
                                                  fields="tracks,next")['tracks']
                       songs = get_songs_from_playlist(tracks, args)
                       download_songs(songs, playlist_folder )
                else:
                    print "No S.N. Provided! Aborting..."
            else:
                print "No Playlist Found!"
        else:
            print "Can't get token for", username
            exit()


if __name__ == '__main__':
    main()
