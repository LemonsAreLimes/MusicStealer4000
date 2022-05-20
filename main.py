from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from pytube import YouTube
import os
import time

import colorama

PlaylistLink = 'your playlist'
DownloadDirectory = 'MusicStealer4000\music'

#spotify finder stuff
content_box_class = 'h4HgbO_Uu1JYg5UGANeQ.wTUruPetkKdWAR1dd6w4'
name_class = 'Type__TypeElement-goli3j-0.fCtMzo.t_yrXoUO3qGsJS4Y6iXX.standalone-ellipsis-one-line'
artist_parent_class = 'Type__TypeElement-goli3j-0.hHrtFe.rq2VQ5mb9SDAFWbBIUIn.standalone-ellipsis-one-line'

#youtube video, used for getting href
youtube_link_parent = 'yt-simple-endpoint.style-scope.ytd-video-renderer'

sev = Service("C:\Program Files (x86)\chromedriver_win32(2)\chromedriver.exe")
op = webdriver.ChromeOptions()
ms4k = webdriver.Chrome(service=sev, options=op)

ms4k.get(PlaylistLink)

print('scroll down pls')
time.sleep(10)
print('okay...')

content_box = ms4k.find_elements(By.CLASS_NAME, content_box_class)


    #get the song names and artist
searchlist = []
for i in range(len(content_box)):
    name = content_box[i].find_element(By.CLASS_NAME, name_class)
    artist = content_box[i].find_element(By.CLASS_NAME, artist_parent_class)
    searchlist.append([name.text, artist.text])


    #goto youtube and download audio
for song in searchlist:
    ms4k.get(f'https://www.youtube.com/results?search_query={song}')

    parent_elem = ms4k.find_element(By.CLASS_NAME, youtube_link_parent)
    link = parent_elem.get_attribute('href')
    
            #lil bit of code theifery here but ur no better if u use this >:)
    try:
        yt = YouTube(link)
        video = yt.streams.filter(only_audio=True).first()
    
        out_file = video.download(output_path=DownloadDirectory)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'

        os.rename(out_file, new_file)
        print(yt.title + f'{colorama.Fore.GREEN} has been successfully downloaded.')

    except FileExistsError:
        print(f'{colorama.Fore.YELLOW}File already exists... moving on')

    except:
        print(f'{colorama.Fore.RED} yeah boss something went wrong here....')

ms4k.close()
