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

# 水名

with open("data/river.json") as f:
    df = json.load(f)

rivers = {}

for area in df:
    obj = df[area]

    for index in obj:
        item = obj[index]

        vol = item["vol"]
        value = item["value"]
        orders = item["order"]

        index = int(index)

        if index not in rivers:
            rivers[index] = {
                "vol" : vol,
                "value" : value,
                "children" : {}
            }

        for order in orders:
            # print(order, area)

            if order.isdecimal():
                order = order.zfill(2)

            children = rivers[index]["children"]

            if order not in children:
                children[order] = []
            children[order].append(area)

arr = []

for index in sorted(rivers):
    item = rivers[index]
    children2 = []
    children = item["children"]
    for key in sorted(children):
        if key.isdecimal():
            key2 = str(int(key))
        else:
            key2 = key
        children2.append({
            "index" : key2,
            "value" : children[key]
        })
    item["children"] = children2
    arr.append(item)

with open("data/river2.json", 'w') as f:
    json.dump(arr, f, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))