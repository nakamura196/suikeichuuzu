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
import requests
import shutil


def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

map = {
    "西域" : "saiiki",
    "越南" : "etsunan",
    "本図" : "main"
}

data = {}

canvases = {}
member_manifest_map = {}

labels = {}

for key in map:
    path = "/Users/nakamurasatoru/git/d_toyo/suikeichuuzu/src/2021/data/curation/"+map[key]+"/raw.json"
    with open(path) as f:
        df = json.load(f)

    manifest = df["selections"][0]["within"]["@id"]

    labels[manifest] = df["selections"][0]["within"]["label"]

    members = df["selections"][0]["members"]

    # membersMap = {}
    # items = []

    for obj in members:
        member_id = obj["@id"]

        label = obj["label"].replace("表", "").replace("裏", "")
        if label not in canvases:
            canvases[label] = []
        canvases[label].append(member_id)

        ##########

        member_manifest_map[member_id] = manifest

        '''
        data[member_id] = {
            "id" : map[key],
            "data": df,
            "manifest": manifest,
            "map" : items # canvases # membersMap
        }
        '''

# print(data)

# 水名

with open("data/river2.json") as f:
    df = json.load(f)

######

for river in df:
    river_label = river["value"]

    curation_uri = "https://nakamura196.github.io/suikeichuuzu/iiif-curation/"+river_label+".json"

    print(river_label)

    children = river["children"]

    tmp = {}

    for child in children:
        areas = child["value"]

        index = child["index"]

        for area in areas:

            if area not in canvases:
                print("missing", area)
                continue

            if area in ["歷城圖", "鄴城圖", "薊城圖", "平城圖", "洛陽城圖", "長安城圖", "睢陽城圖"]:
                continue

            canvas_list = canvases[area]
            for canvas_id in canvas_list:
                manifest = member_manifest_map[canvas_id]

                if manifest not in tmp:
                    tmp[manifest] = []
                tmp[manifest].append({
                    "id" : canvas_id,
                    "index" : index
                })

    selections = []

    for manifest in tmp:
        members = []

        for member in tmp[manifest]:
            member_id = member["id"]
            index = member["index"]

            url = "https://cdn.mapmarker.io/api/v1/pin?size=34&background=%230062B1&text={}&color=%23FFFFFF&voffset=2&hoffset=1".format(index)

            path = "/Users/nakamurasatoru/git/d_toyo/suikeichuuzu/docs/marker/" + str(index) + ".png"

            if not os.path.exists(path):
                download_img(url, path)

            url = "https://nakamura196.github.io/suikeichuuzu/marker/" + str(index) + ".png"

            members.append({
                "@id": member_id,
                "@type": "sc:Canvas",
                "label": index,
                "metadata": [
                    {
                    "value": [
                        {
                        "@id": member_id+"#marker",
                        "on": member_id,
                        "@type": "oa:Annotation",
                        "resource": {
                            "chars": index, # "<a href=\"#\">{}</a>".format(index),
                            "format": "text/html",
                            "@type": "cnt:ContentAsText",
                            "marker": {
                            "@type": "dctypes:Image",
                            "@id": url + "#xy=11,27"
                            }
                        },
                        "motivation": "sc:painting"
                        }
                    ],
                    "label": "Annotation"
                    }
                ],
            })

        manifest_label = labels[manifest]

        selection = {
            "@id": curation_uri + "/range",
            "@type": "sc:Range",
            "label": "Markers",
            "members" : members,
            "within" : {
                "@id" : manifest,
                "@type": "sc:Manifest",
                "label" : manifest_label
            }
        }

        selections.append(selection)

    curation = {
        "@context": [
            "http://iiif.io/api/presentation/2/context.json",
            "http://codh.rois.ac.jp/iiif/curation/1/context.json"
        ],
        "@id": curation_uri,
        "@type": "cr:Curation",
        "label": river_label,
        "viewingHint" : "annotation",
        "selections" : selections
    }

    with open("/Users/nakamurasatoru/git/d_toyo/suikeichuuzu/docs/iiif-curation/"+river_label+".json", 'w') as f:
        json.dump(curation, f, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))