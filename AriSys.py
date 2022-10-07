# 시즌 0 논리.
import json
import random
from copy import deepcopy

# 예외처리는 AriMain.py에서 진행

# 데이터 로딩
with open("area.json", "r") as fl:
    areadata = json.load(fl)

with open("nation.json", "r") as fl:
    nationdata = json.load(fl)

# 최대자원공식(깨질지도)
maxresource = lambda resource: resource * 100

def IDgen(mode="A"): # 간단하게 ID를 만드는 함수
    if "A" in mode or "a" in mode:
        return mode + str(len(areadata))
    if "N" in mode or "n" in mode:
        return mode + str(len(nationdata))

def statgen(min:int=0, max:int=20, len:int=3) -> list:
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

    def __init__(self, ID:str, name:str, food_stat:int, material_stat:int, free_stat:int,
                    food:int, material:int, belongs_to:str, capital:bool): # 이미 있는 데이터
        self.ID = ID
        self.name = name
        self.food_stat = food_stat
        self.material_stat = material_stat
        self.free_stat = free_stat
        self.food = food
        self.material = material
        self.belongs_to = belongs_to #나라명
        self.capital = capital
    
    @staticmethod
    def generate(name=""):
        obj = AriArea(IDgen(), name, *statgen(), 0, 0, "", False)
        return obj
    
    def max_food(self):
        return maxresource(self.food)
    
    def max_material(self):
        return maxresource(self.material)

    def info(self):
        return self.__dict__

class Policy:

    def __init__(self, lv, stat):
        self.lv = lv # 정책의 레벨
        self.stat = stat # 정책에 투자된 스탯 (경험치 비슷)

class unknownpolicy(Policy):

    def __init__(self, lv, stat):
        super().__init__(lv, stat)

class AriNation:

    def __init__(self, culture, tech): #이미 있는 데이터를 끌어오기
        self.culture = culture
        self.tech = tech
    
    @staticmethod
    def generate(culture, tech):
        AriNation(culture, tech)