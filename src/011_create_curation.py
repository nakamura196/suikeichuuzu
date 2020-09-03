
import numpy as np
import math
import sys
import argparse
import json
import html
import requests
import os
from bs4 import BeautifulSoup

title = "水経注図"
legend = "https://nakamura196.github.io/suikeichuuzu/etc/legend.pdf"
curation_id = "https://nakamura196.github.io/suikeichuuzu/curation/test.json"

iconMap = {
    "1" : "https://cdn.mapmarker.io/api/v1/pin?size=30&background=%23009CE0&text=1&color=%23FFFFFF&voffset=2&hoffset=1",
    "5": "https://cdn.mapmarker.io/api/v1/pin?size=30&background=%2373D8FF&text=5&color=%23FFFFFF&voffset=2&hoffset=1",
    "n": "https://cdn.mapmarker.io/api/v1/pin?size=30&background=%23FF7373&text=n&color=%23FFFFFF&voffset=2&hoffset=1"
}

manifest = "https://nakamura196.github.io/suikeichuuzu/iiif/main/manifest.json"

with open('data/oa/items/32605/annolist.json') as f:
    df = json.load(f)

resources = df["resources"]

members = []

for i in range(len(resources)):
    index = str(i + 1)

    resource = resources[i]

    canvas = resource["on"][0]["full"]
    xywh = resource["on"][0]["selector"]["default"]["value"]

    xywhSplitTmp = xywh.split(",")



    memberId = canvas + "#" + xywh
    text = resource["resource"][0]["chars"]
    
    cleantext = BeautifulSoup(text, "lxml").text

    print(cleantext)

    splitTmp = cleantext.split(",")

    if len(splitTmp) > 1:

        冊 = "2"
        図 = splitTmp[0]
        表a裏b = "a"
        図中区画 = splitTmp[1]
        朱z墨m = splitTmp[2]
        図記号 = splitTmp[3]
        地名 = splitTmp[4]
        備考 = ""


        icon = iconMap[splitTmp[3]]+"#xy=15,15"

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
                "value": 冊,
                "label": "冊"
            },
            {
                "value": 図,
                "label": "図"
            },
            {
                "value": 表a裏b,
                "label": "表a裏b"
            },
            {
                "value": 図中区画,
                "label": "図中区画"
            },
            {
                "value": 朱z墨m,
                "label": "朱z墨m"
            },
            {
                "value": 図記号,
                "label": "図記号"
            },
            {
                "value": 地名,
                "label": "地名/記述"
            },
            
        ]

        label = "Marker "+index

    else:
        label = "Marker "+index

        icon = iconMap["n"]+"#xy=15,15"

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
            }
            
        ]

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