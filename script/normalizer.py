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
    name = re.sub(r' \(.*\)', '', name)
    name = name.strip()
    name = name.lower()
    return name


def normalize(dataframes):
    for df in dataframes:
        df['Link'] = df['Link'].transform(normalize_url)
        df['Group'] = df['Group'].transform(normalize_group)