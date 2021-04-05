
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
import copy
import shutil

settings = {
    "saiiki" : {
        "hash" : "600226dc9723af51efb6d9c366b062c3",
        "image" : "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/1_003_Saiiki_grid_l.tif"
    },
    "etsunan" : {
        "hash" : "27fd1a30265116fbe0e6422974209f99",
        "image" : "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/8_004_Etsunan_grid_l.tif"
    },
    "ukou" : {
        "hash" : "6b5ec55ca57758b4c39e1bb90c86d479",
        "image" : "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/Ukou.tif"
    },
    "jouzu01_rekijou" : {
        "hash" : "99a80fdcdc846a12056b9880bdcfc6af"
    },
    "jouzu02_gyoujou" : {
        "hash" : "86fc8366885e58ec808b95d38c01ddb2"
    },
    "jouzu03_rakuyou" : {
        "hash" : "1bd29b910178d0b6379c143a62c9a629"
    },
    "jouzu04_chouan" : {
        "hash" : "c4a34b738d30fe90fe83e78b2bbc9966"
    },
    "jouzu05_suiyou" : {
        "hash" : "97e9257593c4567a69cf86920b455fc8"
    },
    "jouzu06_heijou" : {
        "hash" : "20be61f217fffbc94c12395db4120ec7"
    },
    "jouzu07_keijou" : {
        "hash" : "c9406bab532db460ff8c119d69ad5984"
    },
    "jouzu08_rojou" : {
        "hash" : "65a910994c0d4bc5bec2464c2c5871e3"
    },
    "jouzu09_rinshi" : {
        "hash" : "d1f5a800de359d7d605935a0f0219ea5"
    },
    "jouzu10_jouyou" : {
        "hash" : "b4ee5c48a77b85fa2d9f9d03e7d050fa"
    },
    "jouzu11_jushun" : {
        "hash" : "1056d3b2ef8a61fda18cc3b368e4dad2"
    },
    "jouzu12_seito" : {
        "hash" : "3f6b7a39e8eed39e3925c26362aa7147"
    },
    "jouzu13_sanin" : {
        "hash" : "a47cddf2979d5c7fd527d8336a98affc"
    }
}

uuid = "jouzu13_sanin"

setting = settings[uuid]

# image = setting["image"]

prefix = "https://suikeichu.web.app"

with open('data/metadata.json') as f:
    metadata = json.load(f)

dir = "/Users/nakamurasatoru/git/d_omeka/omekac_diyhistory"

##############

rows = []

key = uuid

hash = setting["hash"]

curation_ids = []

print("***", key)

file = dir + "/docs/iiif/curation/"+hash+"/curation.json"

with open(file) as f:
    curation = json.load(f)

manifest = curation["selections"][0]["within"]["@id"]

m = requests.get(manifest).json()

image = m["sequences"][0]["canvases"][0]["images"][0]["resource"]["service"]["@id"]

members = curation["selections"][0]["members"]

members_map = {}

for member in members:
    label = member["label"]

    label = label.split("&nbsp;")[0].strip()


    if label in curation_ids:
        print("dupppp", label)
        continue
    else:
        curation_ids.append(label)

    if label not in metadata:
        print("not in metadata", label)
        continue

    metadata_new = []

    obj = metadata[label]

    for key in obj:
        value = obj[key]
        
        if value == "null":
            continue

        metadata_new.append({
            "label" : key,
            "value" : obj[key]
        })

    member["metadata"] = metadata_new

    xywh = member["@id"].split("=")[1]

    member["thumbnail"] = image + "/"+xywh+"/200,/0/default.jpg"

    members_map[obj["sort"]] = member

members = []
for sort in sorted(members_map):
    # print("sort", sort)
    members.append(members_map[sort])
curation["selections"][0]["members"] = members


ofile = "data/curation/"+uuid+"/curation.json"

dirname = os.path.dirname(ofile)
os.makedirs(dirname, exist_ok=True)

f2 = open(ofile, 'w')
json.dump(curation, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

# オリジナル
shutil.copyfile(file, ofile.replace("curation.json", "raw.json"))

# テスト
curation_test = copy.deepcopy(curation)

members = curation_test["selections"][0]["members"]

for i in range(len(members)):
    member = members[i]

    id = member["label"]

    map = {}

    if "metadata" not in member:
        print("no metadata", id)
        continue

    for e in member["metadata"]:
        map[e["label"]] = e["value"]
    
    del member["metadata"]

    member["metadata"] = [
        {
            "value": "[ <a href=\"{}\">1-001</a> ]<br/>地名/記述：{}<br/>記号：{}".format(prefix+"/item/"+ id, map["地名/記述"], map["記号"]),
            "label": "Description"
        }
        ]

    ########

    rows.append({
        "id" : id,
        "label" : map["地名/記述"],
        "category" : map["記号"],
        "manifest" : "https://nakamura196.github.io/suikeichuuzu/iiif/"+uuid+"/manifest.json",
        "member" : member["@id"]
    })

curation_test["viewingHint"] = "annotation"
curation_test["related"] = {
    "@type": "cr:MarkerLegend",
    "@id": "http://codh.rois.ac.jp/edo-maps/about/#legend"
}

f2 = open(ofile.replace("curation.json", "test.json"), 'w')
json.dump(curation_test, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

f2 = open("data/rows.json", 'w')
json.dump(rows, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

