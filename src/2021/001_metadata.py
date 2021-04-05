
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

files = [
    "水経注図地名アノテーション01-04-matome20210302.xlsx", 
    "水経注図地名アノテーション05-08-matome20210302.xlsx",
    "水経注図地名アノテーション09Saiiki-matome20210302.xlsx",
    "水経注図地名アノテーション10Etsunan-matome20210302.xlsx",
    "水経注図地名アノテーション11城図-matome20210302.xlsx",
    "水経注図地名アノテーション12禹貢-matome20210302.xlsx"
]

excel_data = {}

def conv(data):
    if pd.isnull(data):
        return "null"
    else:
        return data

count = 0

for i in range(len(files)):
    file = files[i]
    
    # for file in files:

    excel_path = "data/excel/" + file

    df = pd.read_excel(excel_path, sheet_name=0, header=None, index_col=None, engine='openpyxl')

    r_count = len(df.index)
    c_count = len(df.columns)

    for j in range(1, r_count):
        id = df.iloc[j, 0]

        if id in excel_data:
            print("check", id)

        id = id.strip()

        # print(id)
        excel_data[id] = {
            "sort": "{}-{}".format(str(i).zfill(2), str(j).zfill(5)),
            "冊" : conv(df.iloc[j, 1]),
            "図" : conv(df.iloc[j, 2]),
            "区画南北" : conv(df.iloc[j, 3]),
            "区画東西" : conv(df.iloc[j, 4]),
            "表裏" : conv(df.iloc[j, 5]),
            "詳細区画" : conv(df.iloc[j, 6]),
            "墨朱" : conv(df.iloc[j, 7]),
            "記号" : conv(df.iloc[j, 8]),
            "地名/記述" : conv(df.iloc[j, 9]),
            "備考" : conv(df.iloc[j, 10]),
        }

        count += 1

print(count)

with open("data/metadata.json", 'w') as f:
    json.dump(excel_data, f, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))