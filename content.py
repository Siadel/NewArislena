# 시즌 0 논리
from base import *
from pathlib import Path
from sys import modules
import random
from copy import deepcopy

# 예외처리는 AriMain.py에서 진행

# 데이터 로딩 (이거 전역변수임)
path_datas = Path("./datas/")
files = path_datas.glob("*.json")

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

def has_key(data:dict, key:str) -> bool:
    # data에 key가 있으면 True, 없으면 False
    try:
        data[key]
        return True
    except KeyError:
        return False

class AriDataFiles(OnlyOneClass):
    # json에서 가져온 dict 형식 데이터를 직접 관리하는 클래스

    def __init__(self):
        super().__init__()
        # 이하 편집기 인식을 위한 attr 선언
        self.area:dict[str, dict] = None
        self.government:dict[str, dict] = None
        self.military:dict[str, dict] = None
        self.system:dict[str, dict] = None
        for p in list(files):
            data = load_json(p)
            self.__setattr__(str(p).split("\\")[-1].split(".")[0], data) # 확장자를 뺀 파일명이 attribute로 저장됨

    def remove_content(self, key:str, ID:str):
        # ID를 키로 가지는 데이터를 삭제 후 저장
        # ID를 키로 가지는 데이터가 있으면 삭제 후 commit() 실행
        # key는 만들어진 파일명(확장자 제외) 중 하나

        del self.__dict__[key][ID]

        self.save(key)
    
    def add_content(self, key:str, ID:str, **kwargs):

        self.__dict__[key][ID] = kwargs

    def save(self, *args):
        # args에는 "area", "government", "system"이 들어갈 수 있음
        # args에 아무것도 들어가지 않으면 모든 데이터를 save_json()을 이용해 저장
        # 항상 self.commit() 실행

        if len(args) == 0:
            args = ("area", "government", "military", "system")
        for arg in args:
            if arg == "area":
                save_json(self.area, "./datas/area.json")
            elif arg == "government":
                save_json(self.government, "./datas/government.json")
            elif arg == "military":
                save_json(self.military, "./datas/military.json")
            elif arg == "system":
                save_json(self.system, "./datas/system.json")


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
            # 이미 클래스에 존재하는 키를 검색
            # 클래스에 명시되지 않는 키는 애당초 무시됨
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

    def commit_deco(self, func):
        # func를 실행한 뒤 self.commit() 실행
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            self.commit()
        return wrapper

aridatas = AriDataFiles()