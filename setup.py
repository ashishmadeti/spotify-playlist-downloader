from setuptools import setup

long_description = open('README.md').read()

setup(
    name='spotipy_download',
    version='1.0',
    description='Script to download your spotify playlists',
    long_description=long_description,
    author="@ashishmadeti",
    install_requires=[
        'youtube_dl',
        'eyed3',
        'unidecode',
        'spotipy',
    ],
    license='MIT',
    packages=['spotify_download'])
