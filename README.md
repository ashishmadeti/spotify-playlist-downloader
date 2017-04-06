# spotify-playlist-downloader
Download your spotify playlists using simple python script


### Features
* Adds metadata to the downloaded songs (title, artist and album)
* Download only the songs you don't have

### Downloading playlist

* Install dependencies: `pip install youtube_dl eyed3 unidecode bs4` (May require root priveleges)
* Convert your spotify playlists to csv from [here](http://joellehman.com/playlist/) (Thanks to [Joel Lehman](https://github.com/jal278))
* If you don't convert playlist to csv file, give playlist URI, username, and
  access token as commandline argument
* Use [download_from_csv.py](download_from_csv.py) to download all songs from the playlist. (For usage: `python download_from_csv.py -h`)

### Use cases
```
python download_from_csv.py -i csv_file.csv
```
```
python download_from_csv.py -p PLAYLIST_URI -u USERNAME -t AUTHORIZATION_TOKEN
```
```
python download_from_csv.py -p PLAYLIST_URI  #give username and token as input
```
* If you don't have a authorization token, get it
  [here](https://developer.spotify.com/web-api/console/get-playlist-tracks/).

### TODO
I am planning to add more features to this to make the experience more smooth and improve the quality of the downloaded songs. Feel free to open an issue for any bug or enhancement that

- [ ] Allow exporting to CSV from the script itself, will need to ask for spotify login
- [ ] Allow user to specify search terms for youtube (either through config file or through command line arguments)
- [ ] Add Album Art to the downloaded songs
