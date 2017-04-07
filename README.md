# spotify-playlist-downloader
Download your spotify playlists using simple python script


### Features
* Adds metadata to the downloaded songs (title, artist and album)
* Download only the songs you don't have


### Installation
If you already have [Python](http://www.python.org/) on your system you can install the library simply by downloading the distribution, unpack it and install in the usual fashion: (May require root priveleges)

    python setup.py install

### Downloading playlist
>`$ cd spotify_download`
> (For usage: `python download.py -h`)
1. Download through CSV File
    * Convert your spotify playlists to csv from [here](http://joellehman.com/playlist/) (Thanks to [Joel Lehman](https://github.com/jal278))
    * Use [download.py](spotigy_download/download.py) to download all songs from the playlist.
2. Download through user login
    * Login to your spotify account and Create your [Application](https://developer.spotify.com/my-applications/#!/applications)
        * Set Redirect URIs = `http://localhost/` in your application settings and save it.
        * Set environment variables like,

              - export SPOTIPY_CLIENT_ID='your-spotify-client-id'
              - export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
              - export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

### TODO
I am planning to add more features to this to make the experience more smooth and improve the quality of the downloaded songs. Feel free to open an issue for any bug or enhancement that

- [ ] Allow exporting to CSV from the script itself, will need to ask for spotify login
- [ ] Allow user to specify search terms for youtube (either through config file or through command line arguments)
- [ ] Add Album Art to the downloaded songs
