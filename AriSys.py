# 시즌 0 논리.
import json
import random
from copy import deepcopy

# 예외처리는 AriMain.py에서 진행

# 데이터 로딩
with open("area.json", "r") as fl:
    areadata: dict = json.load(fl)

with open("nation.json", "r") as fl:
    nationdata: dict = json.load(fl)

with open("global.json", "r") as fl:
    globaldata: dict = json.load(fl)

def IDgen(mode="A", data_length=1): # 간단하게 ID를 만드는 함수
    if "A" in mode or "a" in mode:
        return mode + str(data_length)
    if "N" in mode or "n" in mode:
        return mode + str(data_length)

def statgen(min:int=0, max:int=20, len:int=7) -> list:
    # 합쳐서 max가 되는 min 이상의 정수(아마도) len개의 리스트 랜덤 생성
    gen = []
    r = [] # 반환할 리스트
    for i in range(len-1):
        gen.append(random.randint(min, max))
    gen.sort(reverse=True)
    genB = deepcopy(gen)
    gen.insert(0, max)
    genB.append(min)
    for a, b in zip(gen, genB):
        r.append(a - b)
    return r


class AriArea:

    def __init__(self, ID:str, area_d:dict): # 이미 있는 데이터
        self.ID = ID
        for k, v in area_d.items():
            setattr(self, k, v)
    
    @staticmethod
    def generate(name=""):
        obj = AriArea(IDgen(len(areadata)), name, *statgen(), 0, 0, "", False)
        return obj

    def info(self):
        return self.__dict__

class AriNation:

    def __init__(self, culture, tech): #이미 있는 데이터를 끌어오기
        self.culture = culture
        self.tech = tech
    
    @staticmethod
    def generate(culture, tech):
        AriNation(culture, tech)