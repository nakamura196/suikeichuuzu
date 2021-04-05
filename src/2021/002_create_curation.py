
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

with open('data/metadata.json') as f:
    metadata = json.load(f)

dir = "/Users/nakamurasatoru/git/d_omeka/omekac_diyhistory"

settings = {
    "水経注図": "110621ea8b112c9a6ea622da37a0f43a",
	"Saiiki": "600226dc9723af51efb6d9c366b062c3",
    "Etsunan": "27fd1a30265116fbe0e6422974209f99",
    "Ukou": "6b5ec55ca57758b4c39e1bb90c86d479",
	"jouzu13_sanin": "a47cddf2979d5c7fd527d8336a98affc",
	"jouzu08_rojou": "65a910994c0d4bc5bec2464c2c5871e3",
	"jouzu04_chouan": "c4a34b738d30fe90fe83e78b2bbc9966",
	"jouzu03_rakuyou": "1bd29b910178d0b6379c143a62c9a629",
	"jouzu07_keijou": "c9406bab532db460ff8c119d69ad5984",
	"jouzu06_heijou": "20be61f217fffbc94c12395db4120ec7",
	"jouzu10_jouyou": "b4ee5c48a77b85fa2d9f9d03e7d050fa",
	"jouzu02_gyoujou": "86fc8366885e58ec808b95d38c01ddb2",
	"jouzu01_rekijou": "99a80fdcdc846a12056b9880bdcfc6af",
	"jouzu09_rinshi": "d1f5a800de359d7d605935a0f0219ea5",
	"jouzu05_suiyou": "97e9257593c4567a69cf86920b455fc8",
	"jouzu12_seito": "3f6b7a39e8eed39e3925c26362aa7147",
	"jouzu11_jushun": "1056d3b2ef8a61fda18cc3b368e4dad2",
}

for key in settings:

    tmp = [
        "CW2(a)D1-11",
        "S1W1(a)A1-04",
        "S1W1(a)B2-08",
        "S1W1(a)C3-05",
        "S3E2(b)C3-12",
        "S10W2(a)A3-06",
        "S1W1(a)B3-11",
        "S3E2(b)C3-13",
        "S1W1(a)B3-10",
        "S1W2(a)B3-04",
        "S9W3(b)A2-16",
        "CW1(a)D2-10",
        "CW1(a)D2-14",
        "S1W8(a)B2-09",
        "S1W1(a)B2-10"
    ]

    ids = []

    for id in metadata:
        if "CT" in id:
            continue

        if id[0] in ["N", "S", "C"]:
            ids.append(id)

    # print(ids)
    print(len(ids))

    curation_ids = []

    print("***", key)
    hash = settings[key]
    file = dir + "/docs/iiif/curation/"+hash+"/curation.json"

    with open(file) as f:
        curation = json.load(f)    

    members = curation["selections"][0]["members"]

    for member in members:
        label = member["label"]

        label = label.split("&nbsp;")[0].strip()


        if label in curation_ids:
            print("dupppp", label)
        else:
            curation_ids.append(label)

        if label not in metadata:

            if label[0] not in ["北", "南", "中"]:
                print("---------------")
                print(label, member["@id"])
                print("---------------")

    for id in ids:
        if id not in curation_ids:
            print("not", id)

    for id in tmp:
        if id not in curation_ids:
            print("not aihara", id)

    break

