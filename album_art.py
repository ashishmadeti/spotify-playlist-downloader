import requests
from bs4 import BeautifulSoup
import StringIO

# user-agents
headers = {
    'User-Agent': 'Mozilla/5.0'
}


def download(song):
    keywords = song['name'] + '+' + song['album'] + '+' + song['artist']
    url = 'https://www.google.co.in/search?q=%s\&tbm=isch' % keywords
    response = requests.get(url, headers=headers)
    htm = response.text
    soup = BeautifulSoup(htm, 'html.parser')
    imageURL = soup.find('img').get('src')
    try:
        response = requests.get(imageURL, stream=True)
    except:
        return None
    output = StringIO.StringIO()
    for chunk in response:
        output.write(chunk)
    return output.getvalue()
