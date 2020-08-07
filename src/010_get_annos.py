
import numpy as np
import math
import sys
import argparse
import json
import html
import requests
import os

prefix = "https://diyhistory.org/public/omekac"
dir = "data"

def saveFile(id):
    data = requests.get(id).json()

    path = id.replace(prefix, dir)

    dirname = os.path.dirname(path)

    os.makedirs(dirname, exist_ok=True)

    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))

    return data

iconMap = {
    "1" : "https://cdn.mapmarker.io/api/v1/pin?size=120&background=%23009CE0&text=1&color=%23FFFFFF&voffset=2&hoffset=1"
}

manifest = "https://diyhistory.org/public/omekac/oa/collections/236/manifest.json"

m_data = saveFile(manifest)

canvases = m_data["sequences"][0]["canvases"]

for canvas in canvases:
    annoList = canvas["otherContent"][0]["@id"]

    saveFile(annoList)
