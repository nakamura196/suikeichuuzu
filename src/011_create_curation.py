
import numpy as np
import math
import sys
import argparse
import json
import html
import requests
import os
from bs4 import BeautifulSoup

iconMap = {
    "1" : "https://cdn.mapmarker.io/api/v1/pin?size=30&background=%23009CE0&text=1&color=%23FFFFFF&voffset=2&hoffset=1"
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

    splitTmp = cleantext.split(",")

    icon = iconMap[splitTmp[3]]+"#xy=15,15"

    member = {
          "label": "Marker "+index,
          "@type": "sc:Canvas",
          "metadata": [
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
          ],
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
  "label": "Marker List",
  "selections": [
    {
      "within": {
        "@id": manifest,
        "@type": "sc:Manifest"
      },
      "@id": "https://nakamura196.github.io/suikeichuuzu/curation/test.json/range1",
      "label": "Markers",
      "members": members,
      "@type": "sc:Range"
    }
  ],
  "@id": "https://nakamura196.github.io/suikeichuuzu/curation/test.json",
  "related": {
    "@type": "cr:MarkerLegend",
    "@id": "https://nakamura196.github.io/suikeichuuzu/etc/legend.pdf"
  }
}

with open("../docs/curation/test.json", 'w') as f:
    json.dump(curation, f, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))