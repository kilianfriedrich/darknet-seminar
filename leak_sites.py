from requests import session, get
from sys import stderr

import csv
import re
import pandas as pd


tor_proxy = 'socks5h://localhost:9050'
log_file = 'out/log.txt'

def log(message: str, file=None):
    print(message, file=file)
    with open(log_file, 'a') as f:
        f.write(message + '\n')

tor = session()
tor.proxies.update({'http': tor_proxy, 'https': tor_proxy})

resp = tor.get('https://check.torproject.org')
if 'Congratulations. This browser is configured to use Tor.' in resp.text:
    log('✅ You are using Tor!')
else:
    log('❌ You are NOT using Tor!', file=stderr)
    exit(1)

# [Ransomfeed](https://ransomfeed.it)

import bs4

ransomfeed = { 'Group': [], 'Link': [], 'Available': [], 'AvailableLabel': [] }
ransomfeed_soup = bs4.BeautifulSoup(get('https://ransomfeed.it/stats.php?page=groups-stats').text)
ransomfeed_soup = ransomfeed_soup.find('tbody')
ransomfeed_soup = ransomfeed_soup.css.select('tr')

for row in ransomfeed_soup:
    name = row.css.select_one('a')
    group_soup = bs4.BeautifulSoup(get(f"https://ransomfeed.it/{name.attrs['href']}").text)
    card = group_soup.css.select_one('.card:nth-child(3)')
    if card is None:
        continue
    for ro in card.css.select('tr:not(:first-child)'):
        ransomfeed['Group'].append(name.text)
        ransomfeed['Link'].append(ro.css.select_one('td:nth-child(1)').text)
        ransomfeed['AvailableLabel'].append('🟢' in ro.css.select_one('td:nth-child(3)').text)
        log(f"Checking {name.text} ({ro.css.select_one('td:nth-child(1)').text})")
        try:
            tor.get(ro.css.select_one('td:nth-child(1)').text, timeout=60)
            ransomfeed['Available'].append(True)
        except:
            ransomfeed['Available'].append(False)

ransomfeed = pd.DataFrame(ransomfeed)
ransomfeed.to_csv('out/ransomfeed.csv', index=False)

# [ransomwarelive](https://www.ransomware.live)

import bs4

ransomwarelive = { 'Group': [], 'Link': [], 'Available': [], 'AvailableLabel': [] }
ransomwarelive_soup = bs4.BeautifulSoup(get('https://www.ransomware.live/groups/').text)
ransomwarelive_soup = ransomwarelive_soup.find('tbody')
ransomwarelive_soup = ransomwarelive_soup.css.select('tr')

for row in ransomwarelive_soup:
    name = row.css.select_one('a')
    group_soup = bs4.BeautifulSoup(get(f"https://www.ransomware.live{name.attrs['href']}").text)
    card = group_soup.css.select_one('tbody')
    if card is None:
        continue
    for ro in card.css.select('tr'):
        ransomwarelive['Group'].append(name.text)
        ransomwarelive['Link'].append(ro.css.select_one('td:nth-child(4)').text)
        ransomwarelive['AvailableLabel'].append('🟢' in ro.css.select_one('td:nth-child(2)').text)
        log(f"Checking {name.text} ({ro.css.select_one('td:nth-child(4)').text})")
        try:
            tor.get(ro.css.select_one('td:nth-child(4)').text, timeout=60)
            ransomwarelive['Available'].append(True)
        except:
            ransomwarelive['Available'].append(False)

ransomwarelive = pd.DataFrame(ransomfeed)
ransomwarelive.to_csv('out/ransomwarelive.csv', index=False)