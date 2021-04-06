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

actions = []

with open("data/river2.json") as f:
    df = json.load(f)

for i in range(len(df)):

    obj = df[i]

    id = obj["value"]

    action = {
        "_id": id,
        "_index": "river",
        "_source": {
            "_label": id,
            "curation": "https://nakamura196.github.io/suikeichuuzu/iiif-curation/"+id+".json",
            "巻": [
                obj["vol"]
            ],
            "通番": [
                i + 1
            ]
        }
    }

    actions.append(action)

    

with open("/Users/nakamurasatoru/git/d_toyo/app/static/data/river/es.json", 'w') as f:
    json.dump(actions, f, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))
