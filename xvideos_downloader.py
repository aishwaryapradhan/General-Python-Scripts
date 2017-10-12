import argparse
import os
import re

import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Download porn videos automatically')
parser.add_argument('-p', '--pref', help='Enter your preferred keyword', required=True)

args = vars(parser.parse_args())

url = "https://www.xvideos.com/"
vid_url = "https://www.xvideos.com"
prefs = {'k': args['pref']}

# main search page
r = requests.get(url, params=prefs)
soup = BeautifulSoup(r.text, "lxml")
divs = soup.find_all('div', {"class": "thumb-block"})
vid_url += divs[4].a['href']
local_name = os.path.basename(vid_url)

# selected video page
r1 = requests.get(vid_url)
vid_soup = BeautifulSoup(r1.text, "lxml")
tag_str = vid_soup.find_all("script")
matches = re.findall(r'html5player.setVideoUrlHigh\(\'(.*?)\'\)', tag_str[7].text)
down_url = matches[0]

# downloading video from extracted source
print("start downloading..")
res = requests.get(down_url, stream=True)
with open(local_name, 'wb') as f:
    for chunk in res.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
            f.flush()
print("finished downloading..")
