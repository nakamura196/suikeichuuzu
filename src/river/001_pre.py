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


excel_path = "/Users/nakamurasatoru/git/d_toyo/suikeichuuzu/data_20201220/水経注図巻・水名-冊・図名対応20201208.xlsx"

df = pd.read_excel(excel_path, sheet_name=0, header=None, index_col=None, engine='openpyxl')

r_count = len(df.index)
c_count = len(df.columns)

fields = {}

for i in range(3, c_count):
    fields[i] = {
        "巻" : df.iloc[2, i],
        "水名" : df.iloc[3, i]
    }

excel_data2 = {}

for j in range(4, r_count):
    key = df.iloc[j, 2]

    excel_data2[key] = {}
    
    for i in fields:
        if not pd.isnull(df.iloc[j, i]):
            excel_data2[key][i-2] = {
                "order" : str(df.iloc[j, i]).split(","),
                "value" : fields[i]["水名"],
                "vol" : fields[i]["巻"]
            }

with open("data/river.json", 'w') as f:
    json.dump(excel_data2, f, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))