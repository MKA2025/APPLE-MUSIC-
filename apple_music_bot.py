import requests
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

def embed_metadata(file_path, title, artist, album):
    audio = MP3(file_path, ID3=EasyID3)
    audio['title'] = title
    audio['artist'] = artist
    audio['album'] = album
    audio.save()



def download_music(url, cookies_path, download_path):
    # This function uses Apple Music cookies to authenticate and download music
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    # Load cookies
    with open(cookies_path, 'r') as file:
        cookies = json.load(file)

    # Sample logic to simulate download (replace with actual API call or scrapping logic)
    response = requests.get(url, headers=headers, cookies=cookies)
    
    if response.status_code == 200:
        file_name = os.path.join(download_path, "downloaded_music.mp3")
        with open(file_name, 'wb') as file:
            file.write(response.content)
        return file_name
    else:
        raise Exception("Failed to download music")
