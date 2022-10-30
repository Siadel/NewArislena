# 시즌 0 논리
from AriBase import *

import random
from copy import deepcopy

# 예외처리는 AriMain.py에서 진행

# 데이터 로딩
ari_area:dict = load_json("./datas/area.json")
ari_nation:dict = load_json("./datas/nation.json")
ari_system:dict = load_json("./datas/system.json")

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

    def info(self) -> dict:
        # whole_info()보다 제한된 정보 반환
        # 반환하는 변수는 returndict임
        # 인스턴스가 Value 오브젝트일 경우 그 오브젝트의 value를 returndict에 setdefault(k, value) 꼴로 추가
        # 인스턴스가 Value 오브젝트가 아닐 경우 인스턴스를 그대로 returndict에 추가

        returndict = dict()

        for k, v in self.__dict__.items():
            # "__"가 k에 포함되어 있으면 그 변수는 private 변수이므로 제외
            if "__" in k:
                continue
            if isinstance(v, Value):
                returndict.setdefault(k, v.value)
            else:
                returndict.setdefault(k, v)

        return returndict

    def whole_info(self) -> dict:
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
                try:
                    v.__dict__ = kwargs[k]
                except KeyError:
                    pass

    def commit(self):
        # 각 클래스에 대응하는 dict 중 self.ID를 키로 가지는 데이터를 self.whole_info()로 대체
        pass

class AriSystem(AriContent, OnlyOneClass):

    def __init__(self):
        AriContent.__init__(self)
        OnlyOneClass.__init__(self)
        self.name = "아리슬레나"
        self.coda = False
        self.major_version = 0
        self.minor_version = 2
        self.author = "Siadel#7457"
        self.areaseq = 0
        self.nationseq = 0
        self.turn = AriTurn()

    def remove_content(self, ID:str, key:str):
        # ID를 키로 가지는 데이터를 삭제 후 저장
        # ID를 키로 가지는 데이터가 없으면 KeyError 발생
        # ID를 키로 가지는 데이터가 있으면 삭제 후 commit() 실행
        # key가 "area"면 ari_area에서 삭제
        # key가 "nation"이면 ari_nation에서 삭제

        if key == "area":
            del ari_area[ID]
        elif key == "nation":
            del ari_nation[ID]

        self.save(key)
    
    def version(self):
        return f"{self.__big_version}.{self.__middle_version}.{self.__small_version}"

    def commit(self):
        for k, v in self.whole_info().items():
            ari_system[k] = v

    def save(self, *args):
        # args에는 "area", "nation", "system"이 들어갈 수 있음
        # args에 아무것도 들어가지 않으면 모든 데이터를 save_json()을 이용해 저장
        # 항상 self.commit() 실행

        self.commit()
        if len(args) == 0:
            args = ("area", "nation", "system")
        for arg in args:
            if arg == "area":
                save_json(ari_area, "./datas/area.json")
            elif arg == "nation":
                save_json(ari_nation, "./datas/nation.json")
            elif arg == "system":
                save_json(ari_system, "./datas/system.json")