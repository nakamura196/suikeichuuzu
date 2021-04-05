
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

excel_path = "data/excel/水経注図凡例20210302.xlsx"

df = pd.read_excel(excel_path, sheet_name=1, header=None, index_col=None, engine='openpyxl')

r_count = len(df.index)
c_count = len(df.columns)

legend = {}

for j in range(2, r_count):
    id = df.iloc[j, 0]

    print(id)

    setting = {
        "分類" : df.iloc[j, 1],
        # "記号" : df.iloc[j, 2],
        "記号形説明" : df.iloc[j, 3],
        "墨朱" : df.iloc[j, 4] if not pd.isnull(df.iloc[j, 4]) else "",
        "記号説明" : df.iloc[j, 5] if not pd.isnull(df.iloc[j, 5]) else "",
        "記号説明詳細" : df.iloc[j, 6] if not pd.isnull(df.iloc[j, 6]) else ""
    }
    
    legend[int(id)] = setting

with open("data/legend.json", 'w') as f:
    json.dump(legend, f, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))