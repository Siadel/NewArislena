# 시즌 0 논리.
from typing import *
from AriBase import *

import random
from copy import deepcopy

# 예외처리는 AriMain.py에서 진행

# 데이터 로딩
ari_area:dict = load_json("./datas/area.json")
ari_nation:dict = load_json("./datas/nation.json")
ari_system:dict = load_json("./datas/system.json")

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


class AriContent(AriBase):

    def __init__(self):
        super().__init__()

    def generate(self):
        # 새로운 객체 생성
        pass

    def info(self) -> dict:
        # AriContent 자료형의 클래스에 있는 모든 인스턴스의 정보를 dict 자료형으로 반환
        # 반환하는 변수는 returndict임
        # 인스턴스가 AriBase 오브젝트일 경우 그 object의 __dict__를 returndict에 추가
        # 인스턴스가 AriBase 오브젝트가 아닐 경우 인스턴스를 그대로 returndict에 추가

        returndict = dict()

        for k, v in self.__dict__.items():
            # "__"가 k에 포함되어 있으면 그 변수는 private 변수이므로 제외
            if "__" in k:
                continue
            if isinstance(v, AriBase):
                returndict.setdefault(k, v.__dict__)
            else:
                returndict.setdefault(k, v)

        return returndict
    
    def port(self, **kwargs):
        # self.__dict__를 돌면서 kwargs에 있는 키가 있으면 그 값을 대입
        # self.__dict__의 key의 타입이 AriBase면, 그 클래스의 __dict__에 self.__dict__[key]를 대입

        for k, v in self.__dict__.items():
            if k in kwargs:
                self.__dict__[k] = kwargs[k]
            if isinstance(v, AriBase):
                v.__dict__ = kwargs[k]

    def commit(self):
        # 각 클래스에 대응하는 dict 중 self.ID를 키로 가지는 데이터를 self.info()로 대체
        pass


class AriSystem(AriContent, OnlyOneClass):
    def __init__(self):
        AriContent.__init__(self)
        OnlyOneClass.__init__(self)
        self.name = "아리슬레나"
        self.__big_version = 0
        self.__middle_version = 0
        self.__small_version = 0
        self.author = "Siadel#7457"

        self.turn = AriTurn()
    
    def version(self):
        return f"{self.__big_version}.{self.__middle_version}.{self.__small_version}"

    def commit(self):
        ari_system = self.info()

    
class AriNation(AriContent):

    def __init__(self):
        pass
    
    def generate(self):
        # 초기화된 나라 객체에 기본 정보 넣기
        pass
    

class AriArea(AriContent):

    def __init__(self):

        self.ID = ""
        self.name = ""
        self.owner = "" # "닉네임#구별자" 형식
        self.capital = False
        self.birth_stamp = 0 # AriSlena.py에서 지정해야 함

        self.population_limit = 0

        self.food = Food()
        self.material = Material()
        self.science = Science()
        self.culture = Culture()
        self.gold = Gold()
        self.adminitration_power = AdministrationPower()

        self.foodfield = FoodField()
        self.materialfield = MaterialField()
        self.sciencefield = ScienceField()
        self.culturefield = CultureField()
        self.commercialfield = CommercialField()
        self.administrationfield = AdministrationField()

        self.amenity = Amenity()
        self.fertility = Fertility()
        self.richness = Richness()
        
    def generate(self):
        # 초기화된 지역 객체에 기본 정보 넣기
        self.ID = IDgen("A", len(ari_area))
        self.name = "지역 " + str(len(ari_area))
        self.owner = "없음"
    
    def stats(self) -> dict:
        r = dict()
        for k, v in self.__dict__.items():
            if "stat" in k:
                r.setdefault(k, v)
        return r

    def commit(self):
        ari_area[self.ID] = self.info()