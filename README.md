# spotify-playlist-downloader
Download your spotify playlists using simple python script


### Features
* Adds metadata to the downloaded songs (title, artist and album)
* Download only the songs you don't have

### Downloading playlist

* Install dependencies: `pip install youtube_dl eyed3 unidecode` (May require root priveleges)
* Convert your spotify playlists to csv from [here](http://joellehman.com/playlist/) (Thanks to [Joel Lehman](https://github.com/jal278))
* Use [download_from_csv.py](download_from_csv.py) to download all songs from the playlist. (For usage: `python download_from_csv.py -h`)

### Note
* If you build your own packages, then make sure to build FFmpeg (that youtube-dl uses) using the '--enable-libmp3lame' option

### TODO
I am planning to add more features to this to make the experience more smooth and improve the quality of the downloaded songs. Feel free to open an issue for any bug or enhancement that

- [ ] Allow exporting to CSV from the script itself, will need to ask for spotify login
- [x] Allow user to specify search terms for youtube (either through config file or through command line arguments)
- [x] Add Album Art to the downloaded songs
