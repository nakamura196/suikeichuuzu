
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

prefix = "https://suikeichu.web.app"

with open('data/metadata.json') as f:
    metadata = json.load(f)

dir = "/Users/nakamurasatoru/git/d_omeka/omekac_diyhistory"

settings = {
    "水経注図": "110621ea8b112c9a6ea622da37a0f43a"
}

rows = []

for key in settings:

    curation_ids = []

    print("***", key)
    hash = settings[key]
    file = dir + "/docs/iiif/curation/"+hash+"/curation.json"

    with open(file) as f:
        curation = json.load(f)

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

        member["thumbnail"] = "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/Suikeichuuzu.tif/"+xywh+"/200,/0/default.jpg"

        members_map[obj["sort"]] = member

    members = []
    for sort in sorted(members_map):
        print(sort)
        members.append(members_map[sort])
    curation["selections"][0]["members"] = members

    
    ofile = "data/curation/main/curation.json"

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
            "manifest" : "https://nakamura196.github.io/suikeichuuzu/iiif/main/manifest.json",
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

    break

