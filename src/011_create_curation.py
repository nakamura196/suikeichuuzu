
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

title = "水経注図"
legend = "https://nakamura196.github.io/suikeichuuzu/etc/legend.pdf"
curation_id = "https://nakamura196.github.io/suikeichuuzu/curation/test.json"

iconMap = {}

for i in range(0, 33):
    iconMap[str(i)] = "https://cdn.mapmarker.io/api/v1/pin?size=30&background=%23{}&text={}&color=%23FFFFFF&voffset=2&hoffset=1".format("009CE0", i)

manifest = "https://nakamura196.github.io/suikeichuuzu/iiif/main/manifest.json"

excel_path = "../data_20201220/水経注図地名アノテーション01-04-matome20201217.xlsx"

df = pd.read_excel(excel_path, sheet_name=0, header=None, index_col=None, engine='openpyxl')

# 

r_count = len(df.index)
c_count = len(df.columns)

excel_data = {}

for j in range(1, r_count):
    id = df.iloc[j, 0]
    print(id)
    excel_data[id] = {
        "冊" : df.iloc[j, 1],
        "図" : df.iloc[j, 2],
        "区画南北" : df.iloc[j, 3],
        "区画東西" : df.iloc[j, 4],
        "表裏" : df.iloc[j, 5],
        "詳細区画" : df.iloc[j, 6],
        "墨朱" : df.iloc[j, 7],
        "記号" : df.iloc[j, 8],
        "地名/記述" : df.iloc[j, 9],
        "備考" : df.iloc[j, 10],
    }

files = glob.glob("data/oa/items/*/annolist.json")

resources = []

for file in files:

    with open(file) as f:
        df = json.load(f)

    _resources = df["resources"]
    print(file, len(_resources))

    for res in _resources:
        resources.append(res)
        

# resources = df["resources"]

members = []

for i in range(len(resources)):
    index = str(i + 1)

    if i % 1000 == 0:
        print(index, len(resources))

    resource = resources[i]

    canvas = resource["on"][0]["full"]
    xywh = resource["on"][0]["selector"]["default"]["value"]

    xywhSplitTmp = xywh.split(",")



    memberId = canvas + "#" + xywh
    text = resource["resource"][0]["chars"]
    
    cleantext = BeautifulSoup(text, "lxml").text.strip()

    # print(cleantext)

    splitTmp = cleantext.split(",")

    # -----------

    if cleantext not in excel_data:
        print("err", cleantext)
        continue

    m_data = excel_data[cleantext]

    
    label = "Marker "+index

    no = m_data["記号"]

    icon = iconMap[str(no)]+"#xy=15,15"

    # -------

    metadata = [
        {
            "value": [
            {
                "motivation": "sc:painting",
                "resource": {
                "chars": text,
                "@type": "cnt:ContentAsText",
                "format": "text/html",
                "marker": {
                    "@id": icon,
                    "@type": "dctypes:Image"
                }
                },
                "@id": memberId+"_",
                "on": memberId,
                "@type": "oa:Annotation"
            }
            ],
            "label": "Annotation"
        },
        {
            "value": m_data["冊"],
            "label": "冊"
        },
        {
            "value": m_data["図"],
            "label": "図"
        },
        {
            "value": m_data["区画南北"],
            "label": "区画南北"
        },
        {
            "value": m_data["区画東西"],
            "label": "区画東西"
        },
        {
            "value": m_data["表裏"],
            "label": "表a裏b"
        },
        {
            "value": m_data["詳細区画"],
            "label": "詳細区画"
        },
        {
            "value": m_data["墨朱"],
            "label": "朱z墨m"
        },
        {
            "value": m_data["記号"],
            "label": "図記号"
        },
        {
            "value": m_data["地名/記述"],
            "label": "地名/記述"
        }
        
    ]

    if not pd.isnull(m_data["備考"]):
        metadata.append({
            "value":  m_data["備考"],
            "label": "備考"
        })
        

    member = {
          "label": label,
          "@type": "sc:Canvas",
          "metadata": metadata,
          "@id": memberId
        }

    members.append(member)


curation = {
  "@type": "cr:Curation",
  "viewingHint": "annotation",
  "@context": [
    "http://iiif.io/api/presentation/2/context.json",
    "http://codh.rois.ac.jp/iiif/curation/1/context.json"
  ],
  "label": title,
  "selections": [
    {
      "within": {
        "@id": manifest,
        "@type": "sc:Manifest"
      },
      "@id": curation_id + "/range1",
      "label": "Markers",
      "members": members,
      "@type": "sc:Range"
    }
  ],
  "@id": curation_id,
  "related": {
    "@type": "cr:MarkerLegend",
    "@id": legend
  }
}

with open("../docs/curation/test.json", 'w') as f:
    json.dump(curation, f, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))