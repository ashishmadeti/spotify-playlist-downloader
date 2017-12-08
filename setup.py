from setuptools import setup, find_packages

setup(
    name='download_spotify_playlist',
    version='1.0',
    description='Script to download your spotify playlists',
    author="Ashish Madeti",
    author_email="ashishmadeti@gmail.com",
    install_requires=[
        'youtube_dl',
        'eyed3',
        'requests',
        'unidecode',
        'spotipy',
    ],
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['download_spotify_playlist = download_spotify_playlist.download:main'],
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
)
