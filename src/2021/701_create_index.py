
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

app_prefix = "https://suikeichu.web.app"

files = glob.glob('data/curation/*/curation.json')



id_map = {}

for file in files:

    with open(file) as f:
        curation = json.load(f)    

    manifest = curation["selections"][0]["within"]["@id"]

    for member in curation["selections"][0]["members"]:
        id = member["label"]

        id = id.replace("&nbsp;", "").replace("\n", "").strip()

        map = {}

        if "metadata" not in member:
            continue

        metadata = member["metadata"]

        for e in metadata:
            map[e["label"]] = e["value"]

        obj = {
            "_label": map["地名/記述"],
            "_url" : app_prefix + "/item/"+id,
            "_member": member["@id"],
            "_manifest" : manifest,
        }

        # if "thumbnail" in member:
        obj["_thumbnail"] = member["thumbnail"]

        for key in map:
            obj[key] = [map[key]]

        dir = file.split("/")[-2]

        if dir not in id_map:
            id_map[dir] = {}

        id_map[dir][map["sort"]] = {
            "_index": "main",
            "_id": id,
            "_source" : obj
        }

actions = []

for dir in sorted(id_map):

    actions_e = []

    for id in sorted(id_map[dir]):
        actions.append(
            id_map[dir][id]
        )

        actions_e.append(
            id_map[dir][id]
        )

    with open("data/es/"+dir+".json", 'w') as outfile:
        json.dump(actions_e, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

with open("data/es.json", 'w') as outfile:
    json.dump(actions, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))