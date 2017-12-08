from setuptools import setup

long_description = open('README.md').read()

setup(
    name='download_spotify_playlist',
    version='1.0',
    description='Script to download your spotify playlists',
    long_description=long_description,
    author="@ashishmadeti",
    #author_email='',
    install_requires=[
        'youtube_dl',
        'eyed3',
        'unidecode',
        'spotipy',
    ],
    license='MIT',
    packages=['download_spotify_playlist'],
    entry_points={
        'console_scripts': ['download_spotify_playlist = download_spotify_playlist.download:main'],
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
)
