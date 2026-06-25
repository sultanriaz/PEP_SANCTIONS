import pandas as pd
import  pathlib
import sys
import os
project_root = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(project_root))
from src.matcher import find_matches

df = pd.read_csv("data/watchlist.csv")

result = find_matches("Ahmad Khan", df)

for match in result:
    print(match)