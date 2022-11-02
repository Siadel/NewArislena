#from AriProduceable import *
#
#gr = Grassland()
#gr.generate()

import pathlib
import json

path_datas = pathlib.Path("./datas/")
files = path_datas.glob("*.json")

for p in list(files):
    print(p)
    with open(p, "r", encoding="UTF-8") as f:
        data = json.load(f)
        print(data)