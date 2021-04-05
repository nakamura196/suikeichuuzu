
import numpy as np
import math
import sys
import argparse
import json
import html
import requests
import os
from bs4 import BeautifulSoup
import glob
import pandas as pd
import urllib.parse

files = glob.glob("data/es/*.json")

settings = {}

for file in files:
    with open(file) as f:
        es = json.load(f)

    settings[file.split("/")[-1].split(".")[0]] = {
        "label" : es[0]["_source"]["図"][0]
    }

with open("data/settings.json", 'w') as f:
    json.dump(settings, f, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))