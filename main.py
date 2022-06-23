from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from pytube import YouTube
import os
import time
import keyboard
import colorama

PlaylistLink = 'your playlist link goes here'
DownloadDirectory = 'MusicStealer4000\music'

#spotify finder stuff
content_box_class = 'h4HgbO_Uu1JYg5UGANeQ.wTUruPetkKdWAR1dd6w4'
name_class = 'Type__TypeElement-goli3j-0.fCtMzo.t_yrXoUO3qGsJS4Y6iXX.standalone-ellipsis-one-line'
artist_parent_class = 'Type__TypeElement-goli3j-0.hHrtFe.rq2VQ5mb9SDAFWbBIUIn.standalone-ellipsis-one-line'

#youtube video, used for getting href
youtube_link_parent = 'yt-simple-endpoint.style-scope.ytd-video-renderer'

#make sure your chomedriver version matches your current chome version
sev = Service("your chrome driver path")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=sev, options=op)

driver.get(PlaylistLink)

print('initalized')
time.sleep(3)
print(f'{colorama.Fore.GREEN} executing....')



#get the total number of songs in the playlist
song_number_str = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div/section/div[1]/div[5]/div/span[2]').text.rsplit(" ")
song_number = int(song_number_str[0])

print(f'{colorama.Fore.RED} CLICK ONTO THE WINDOW!!!!!!!!!!!!!!!')
print(f'{colorama.Fore.RED} CLICK ONTO THE WINDOW!!!!!!!!!!!!!!!')
print(f'{colorama.Fore.RED} CLICK ONTO THE WINDOW!!!!!!!!!!!!!!!')
time.sleep(1)



namelist = []           #all of the song names
artistlist = []         #all of the artist names
albumlist = []          #not implomented yet
coverlist = []          #not implomented yet

#get all of the songs in the playlist
while True:

    #get all viewable songs
    content_box = driver.find_elements(By.CLASS_NAME, content_box_class)
    for elem in range(len(content_box)):
        try:
            title = content_box[elem].find_element(By.CLASS_NAME, name_class).text
            artist = content_box[elem].find_element(By.CLASS_NAME, artist_parent_class).text

            #prevent dupelicates from going on the list
            if title in namelist:
                pass
            else:
                print(f'{colorama.Fore.BLUE}{len(namelist)}: {colorama.Fore.GREEN}{title}')
                artistlist.append(artist)
                namelist.append(title)

        except:
            print(f'{colorama.Fore.YELLOW}something went wrong.... its ok tho')

    #prevents from endlessly pressing down
    if len(namelist) == song_number:
        print(f'{colorama.Fore.MAGENTA}done grabbing songs, time to download!')
        break

    else:
        keyboard.press_and_release('down')
        keyboard.press_and_release('down')
        keyboard.press_and_release('down')
        keyboard.press_and_release('down')
        keyboard.press_and_release('down')
        keyboard.press_and_release('down')



#download songs
for x in range(len(namelist)):

    #parse the link so its valad
    search_term = namelist[x].replace(" ", "+") + "+" + artistlist[x].replace(" ", "+")
    page_link = f'https://www.youtube.com/results?search_query={search_term}'

    #goto youtube with song name
    driver.get(page_link)

    time.sleep(0.1)

    #get the first results link
    parent_elem = driver.find_element(By.CLASS_NAME, youtube_link_parent)
    href = parent_elem.get_attribute('href')


    try:
        #i dont know what this does i didnt write it 
        yt = YouTube(href)
        video = yt.streams.filter(only_audio=True).first()
    
        out_file = video.download(output_path=DownloadDirectory)
        base, ext = os.path.splitext(out_file)
        new_file = namelist[x] + '.mp3'

        os.rename(out_file, new_file)
        print(f'{colorama.Fore.GREEN} {yt.title} has been successfully downloaded.')

    except FileExistsError:
        print(f'{colorama.Fore.YELLOW}File already exists... moving on')

    except:
        print(f'{colorama.Fore.RED} yeah boss something went wrong here....')


driver.close()
