import re
from urllib.parse import urlparse

import pandas as pd


def normalize_url(url):
    if pd.isna(url):
        return None
    netloc = urlparse(url.strip()).netloc
    if len(netloc.strip()) == 0:
        return url.strip()
    return netloc

def normalize_group(name):
    name = re.search(r"(.*?)( \(.*)?$", name.lower().strip())
    name = name.group(1)
    name = name.replace(' - new', '')
    name = name.replace(' locker', '')
    name = name.replace(' archives', '')
    name = name.replace('-data', '')
    name = name.replace(' security', '')
    name = name.replace(' media', 'media')
    name = name.replace(' vault', 'vault')
    name = name.replace(' vault', 'vault')
    name = name.replace('donut blog', 'donutleaks')
    name = name.replace('donut dls', 'donutleaks')
    name = name.replace('dragon force', 'dragonforce')
    name = name.replace('el dorado/blacklock', 'el dorado')
    name = name.replace('eldorado', 'el dorado')
    name = name.replace(' international', '')
    name = name.replace('kelvinsecurity', 'kelvin')
    name = name.replace('kill 3.0', 'killsec3')
    name = name.replace('killsecurity', 'killsec')
    name = name.replace('lockbit 3.0', 'lockbit3')
    name = name.replace('lockbit3_fs', 'lockbit3')
    name = name.replace('malek team', 'malekteam')
    name = name.replace('money message', 'moneymessage')
    name = name.replace('moses staff', 'mosesstaff')
    name = name.replace('mydata / alpha', 'mydata')
    name = name.replace('ragnar_locker', 'ragnarlocker')
    name = name.replace('ragnar', 'ragnarlocker')
    name = name.replace('ra group', 'ragroup')
    name = name.replace('ransom house', 'ransomhouse')
    name = name.replace('ransom hub', 'ransomhub')
    name = name.replace('ra world', 'raworld')
    name = name.replace('space bears', 'spacebears')
    name = name.replace('team ', '')
    name = name.replace('vanirgroup', 'vanir group')
    name = name.replace('vanir', 'vanir group')
    name = name.replace('werewolves group', 'werewolves')
    return name


def normalize(*dataframes):
    for df in dataframes:
        df['Link'] = df['Link'].transform(normalize_url)
        df['Group'] = df['Group'].transform(normalize_group)