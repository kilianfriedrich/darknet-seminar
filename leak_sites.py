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
        tor.get('http://' + row[' location '].strip(), timeout=60)
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
        tor.get('http://' + row[' location '].strip(), timeout=60)
        ransomfind['Available'].append(True)
    except:
        ransomfind['Available'].append(False)

ransomfind = pd.DataFrame(ransomfind)
ransomfind['Available'] = ransomfind['Available'].astype('bool')
ransomfind.to_csv('out/ransomfind.csv', index=False)