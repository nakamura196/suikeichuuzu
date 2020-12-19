
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

ids = [236, 238, 256, 257, 258, 260, 261, 262, 263, 264, 265]

for id in ids:

    print(id)

    manifest = "https://diyhistory.org/public/omekac/oa/collections/{}/manifest.json".format(id)

    m_data = saveFile(manifest)

    canvases = m_data["sequences"][0]["canvases"]

    for canvas in canvases:
        annoList = canvas["otherContent"][0]["@id"]

        saveFile(annoList)
