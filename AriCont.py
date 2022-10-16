# 시즌 0 논리.
from typing import *
from AriBase import *

import json
import random
from copy import deepcopy

# 예외처리는 AriMain.py에서 진행

# 데이터 로딩
with open("./datas/area.json", "r") as fl:
    whole_area: dict = json.load(fl)

with open("./datas/nation.json", "r") as fl:
    whole_nation: dict = json.load(fl)

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


class AriContents:

    def generate(self, ID:str, data:dict): # 이미 있는 데이터
        pass
    
    def info(self) -> dict[str, Any]:
        return self.__dict__
    
    def stats(self):
        pass

class AriArea(AriContents):

    def __init__(self, areadata=dict()):
        self.ID = ""
        self.name = ""
        self.owner = ""
        self.capital = False

        self.food = Food()
        self.material = Material()
        self.science = Science()
        self.culture = Culture()
        self.gold = Gold()
        self.adminitration_power = AdministrationPower()

        self.amenity = Amenity(self.calc_amenity())
        self.fertility = Fertility()
        self.richness = Richness()
        
    
    def calc_amenity(self):
        return 0
    
    def calc_population(self):
        pass

    def stats(self) -> dict:
        r = dict()
        for k, v in self.__dict__.items():
            if "stat" in k:
                r.setdefault(k, v)
        return r

class AriNation(AriContents):

    def __init__(self):
        pass
    
    def generate(self, ID:str, nationdata:dict): # 이미 있는 데이터
        super().__init__(ID, nationdata)
    
