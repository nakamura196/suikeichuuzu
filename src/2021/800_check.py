
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

with open('data/metadata.json') as f:
    metadata = json.load(f)

ms = []

for key in metadata:
    ms.append(key)

with open('data/es.json') as f:
    es = json.load(f)

ess = []
for item in es:
    id = item["_id"]

    if "nbsp" in id:
        print(id)

    id = id.replace("&nbsp;", "").replace("\n", "").strip()

    ess.append(id)

for key in ms:
    if key not in ess:
        print("Missing", key, metadata[key]["図"])

