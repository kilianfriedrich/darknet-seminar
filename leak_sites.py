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

# [fastfire/deepdarkCTI](https://github.com/fastfire/deepdarkCTI/blob/main/ransomware_gang.md)

deepdarkcti_md = get('https://raw.githubusercontent.com/fastfire/deepdarkCTI/refs/heads/main/ransomware_gang.md').text
lines = deepdarkcti_md.splitlines()
lines.pop(1) # Header-Endzeile entfernen
lines = [line.strip('|') for line in lines] # '|' Am Anfang und Ende der Zeile entfernen

deepdarkcti_reader = csv.DictReader(lines, delimiter='|')

deepdarkcti = { 'Group': [], 'Link': [], 'Available': [], 'AvailableLabel': [] }
for row in deepdarkcti_reader:
    parsed_name = re.search(r"\[([^]]*)]\(([^)]*)\)", row['Name'])
    if parsed_name is not None:
        if parsed_name.group(1) in [
            'Ransomfeed',
            'eCrime Services',
            'RANSOM DB',
            'RANSOMWARE GROUP SITES (list)',
            'RANSOMWARE GROUPS MONITORING TOOL',
            'RansomChats'
        ]:
            continue
        deepdarkcti['Group'].append(parsed_name.group(1))
        deepdarkcti['Link'].append(parsed_name.group(2))
        deepdarkcti['AvailableLabel'].append('ONLINE' in row['Status'])
        log(f"Checking {parsed_name.group(1)} ({parsed_name.group(2)})")
        try:
            tor.get(parsed_name.group(2), timeout=60)
            deepdarkcti['Available'].append(True)
        except:
            deepdarkcti['Available'].append(False)

deepdarkcti = pd.DataFrame(deepdarkcti)
deepdarkcti.to_csv('out/deepdarkcti.csv', index=False)

# [u/DrinkMoreCodeMore](https://www.reddit.com/r/Malware/comments/1bpcrdw/list_of_ransomware_groups_and_their_pr_pages_2024)

import bs4

reddit2024_soup = bs4.BeautifulSoup(get('https://www.reddit.com/r/Malware/comments/1bpcrdw/list_of_ransomware_groups_and_their_pr_pages_2024/').text)
reddit2024_soup = reddit2024_soup.css.select('shreddit-post [slot=text-body] > div > div > p')

reddit2024 = { 'Group': [], 'Link': [], 'Available': [] }
for p in reddit2024_soup:
    if p.find('a') is None:
        continue
    parsed_text = re.search(r"([^]]*) - ([^)]*)", p.text)
    if parsed_text is not None:
        reddit2024['Group'].append(parsed_text.group(1).strip())
        reddit2024['Link'].append(parsed_text.group(2).strip())
        log(f"Checking {parsed_text.group(1).strip()} ({parsed_text.group(2).strip()})")
        try:
            tor.get(parsed_text.group(2).strip(), timeout=60)
            reddit2024['Available'].append(True)
        except:
            reddit2024['Available'].append(False)

reddit2024 = pd.DataFrame(reddit2024)
reddit2024.to_csv('out/reddit2024.csv', index=False)

# [Onion-Seite](http://ransomwr3tsydeii4q43vazm7wofla5ujdajquitomtd47cxjtfgwyyd.onion)

import bs4

darknet_soup = bs4.BeautifulSoup(tor.get('http://ransomwr3tsydeii4q43vazm7wofla5ujdajquitomtd47cxjtfgwyyd.onion/').text)
darknet_soup = darknet_soup.css.select_one('.table .table-body')
darknet_soup = darknet_soup.css.select('.table-row')

darknet = { 'Group': [], 'Link': [], 'Available': [] }
for row in darknet_soup:
    name = row.css.select_one('.table-cell')
    links = row.css.select('a')
    for link in links:
        darknet['Group'].append(name.text)
        darknet['Link'].append(link.attrs['href'])
        log(f"Checking {name.text} ({link.attrs['href']})")
        try:
            tor.get(link.attrs['href'], timeout=60)
            darknet['Available'].append(True)
        except:
            darknet['Available'].append(False)

darknet = pd.DataFrame(darknet)
darknet.to_csv('out/darknet.csv', index=False)

# [Ransomwatch](https://ransomwatch.telemetry.ltd)

import csv

ransomwatch_md = get('https://ransomwatch.telemetry.ltd/INDEX.md').text
lines = ransomwatch_md.splitlines()[2:-1]
lines.pop(1) # Header-Endzeile entfernen
lines = [line.strip('|') for line in lines] # '|' Am Anfang und Ende der Zeile entfernen

ransomwatch_reader = csv.DictReader(lines, delimiter='|')

ransomwatch = { 'Group': [], 'Available': [], 'Link': [], 'AvailableLabel': [] }
for row in ransomwatch_reader:
    if len(row[' group '].strip()) == 0:
        continue
    parsed_name = re.search(r"\[([^]]*)]\(([^)]*)\)", row[' group '])
    ransomwatch['Group'].append(parsed_name.group(1))
    ransomwatch['Link'].append(row[' location '])
    if row[' status '] is not None:
        ransomwatch['AvailableLabel'].append('🟢' in row[' status '])
    else:
        ransomwatch['AvailableLabel'].append(False)
    log(f"Checking {parsed_name.group(1)} ({row[' location ']})")
    try:
        tor.get(row[' location '], timeout=60)
        ransomwatch['Available'].append(True)
    except:
        ransomwatch['Available'].append(False)


ransomwatch = pd.DataFrame(ransomwatch)
ransomwatch['Available'] = ransomwatch['Available'].astype('bool')
ransomwatch.to_csv('out/ransomwatch.csv', index=False)

# [Ransomfind](https://ransomfind.io)

import csv

ransomfind_md = get('https://ransomfind.io/INDEX.md').text
lines = ransomfind_md.splitlines()[2:-1]
lines.pop(1) # Header-Endzeile entfernen
lines = [line.strip('|') for line in lines] # '|' Am Anfang und Ende der Zeile entfernen

ransomfind_reader = csv.DictReader(lines, delimiter='|')

ransomfind = { 'Group': [], 'Available': [], 'Link': [], 'AvailableLabel': [] }
for row in ransomfind_reader:
    parsed_name = re.search(r"\[([^]]*)]\(([^)]*)\)", row[' group '])
    ransomfind['Group'].append(parsed_name.group(1))
    ransomfind['Link'].append(row[' location '].strip())
    ransomfind['AvailableLabel'].append('🟢' in row[' status '])
    log(f"Checking {parsed_name.group(1)} ({row[' location '].strip()})")
    try:
        tor.get(row[' location '].strip(), timeout=60)
        ransomfind['Available'].append(True)
    except:
        ransomfind['Available'].append(False)

ransomfind = pd.DataFrame(ransomfind)
ransomfind['Available'] = ransomfind['Available'].astype('bool')
ransomfind.to_csv('out/ransomfind.csv', index=False)

# [Ransomlook](https://www.ransomlook.io)

import bs4

ransomlook_soup = bs4.BeautifulSoup(get('https://www.ransomlook.io/groups').text)

ransomlook = { 'Group': [], 'Available': [], 'Link': [], 'AvailableLabel': [] }
for header in ransomlook_soup.css.select('h3'):
    following = header.find_next('div')
    if following is not None:
        links = following.css.select_one('tbody')
        for link in links.css.select('tr'):
            ransomlook['Group'].append(header.text)
            ransomlook['Link'].append(link.css.select_one('td:nth-child(4)').text)
            ransomlook['AvailableLabel'].append('⬆️' in link.css.select_one('td:nth-child(2)').text)
            log(f"Checking {header.text} ({link.css.select_one('td:nth-child(4)').text})")
            try:
                tor.get(link.css.select_one('td:nth-child(4)').text, timeout=60)
                ransomlook['Available'].append(True)
            except:
                ransomlook['Available'].append(False)

ransomlook = pd.DataFrame(ransomlook)
ransomlook['Available'] = ransomlook['Available'].astype('bool')
ransomlook.to_csv('out/ransomlook.csv', index=False)


# [Ransomfeed](https://ransomfeed.it)

import bs4

ransomfeed = { 'Group': [], 'Link': [], 'Available': [], 'AvailableLabel': [] }
ransomfeed_soup = bs4.BeautifulSoup(get('https://ransomfeed.it/stats.php?page=groups-stats').text)
ransomfeed_soup = ransomfeed_soup.find('tbody')
ransomfeed_soup = ransomfeed_soup.css.select('tr')

for row in ransomfeed_soup:
    name = row.css.select_one('a')
    group_soup = bs4.BeautifulSoup(get(f"https://ransomfeed.it{name.attrs['href']}").text)
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