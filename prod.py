from cont import *

def has_coda(number:str|int):
    # 한국 한자음으로 숫자를 읽었을 때 종성이 있는지 없는지를 출력
    # number는 numeric으로 끝나는 str 혹은 int여야 함
    # number를 str로 변환
    # number가 0으로 끝나고 13자리 이상, 16자리 이하면 False
    # number가 0으로 끝나는 나머지 경우는 True
    # number가 1, 3, 6, 7, 8로 끝나면 True
    # number가 0과 1, 3, 6, 7, 8을 제외한 나머지 숫자로 끝나면 False

    number = str(number)
    if number[-1] == "0":
        if len(number) >= 13 and len(number) <= 16:
            return False
        else:
            return True
    elif number[-1] in ["1", "3", "6", "7", "8"]:
        return True
    else:
        return False

class Manageable(AriContent):

    ari_data = dict()
    data = dict()

    def __init__(self):
        super().__init__()
        self.name = None
        self.ID = ""
        self.birth_stamp = 0  # ari_systemlena.py에서 지정해야 함
        self.dominator: str|None = None # 지도부 ID

    def change_name(self, new_name):
        self.name = new_name

    def generate(self):
        # 새로운 객체 생성
        raise Exception("Not Implemented")

    def commit(self):
        self.data[self.ID] = self.whole_info()

class Machine(Manageable):
    # 자원을 소모하고 산출하는 녀석. 네이밍을 뭐로 해야 할지 모르겠다

    def __init__(self):
        super().__init__()
        self.food_cost = 0
        self.material_cost = 0
        self.food_produce = 0
        self.material_produce = 0
        self.power_produce = 0

class Military(Machine):
    
    data = aridatas.military

    def __init__(self):
        super().__init__()
        self.term = "군사"

        self.food_cost = 1
        self.material_cost = 1

        self.power_produce = 0

        self.location = "" # 지역 ID

    def generate(self, *, name:str|None=None, power:int=0, location:str="", dominator:str|None=None, coda:bool=True):
        self.ID = ari_system.IDgen("M")
        self.name = "군사 " + str(ari_system.militaryseq) if name is None else name
        self.power = power
        self.location = location
        self.dominator = dominator
        self.coda = has_coda(self.name) if coda is None and name is None else coda
        ari_system.militaryseq += 1
        ari_military[self.ID] = self
        self.commit()
        ari_system.commit()


class AriArea(Machine):

    data = aridatas.area

    def __init__(self):
        super().__init__()
        self.term = "지역"
        self.capital: bool = False
        self.level = 0
        self.supply_produce = 0
        self.resistance_power = 0
        self.history = []
        
    def generate(self, *, name:str|None=None, dominator:str|None=None, coda:bool=True):
        # 초기화된 지역 객체에 기본 정보 넣기
        self.ID = ari_system.IDgen("A")
        self.name = "지역 " + str(ari_system.areaseq) if name is None else name
        self.dominator = dominator
        self.coda = has_coda(self.name) if coda is None and name is None else coda
        ari_system.areaseq += 1
        ari_area[self.ID] = self
        self.commit()
        ari_system.commit()

class WildArea(AriArea):

    def __init__(self):
        super().__init__()

class Grassland(WildArea):

    def __init__(self):
        super().__init__()
        self.term = "초원"
        self.food_produce = 1
        self.supply_produce = 1
        self.resistance_power = 1

class Plain(WildArea):

    def __init__(self):
        super().__init__()
        self.term = "평원"
        self.food_produce = 2
        self.resistance_power = 1

class Forest(WildArea):

    def __init__(self):
        super().__init__()
        self.term = "수림"
        self.material_produce = 1
        self.resistance_power = 2

class Hill(WildArea):

    def __init__(self):
        super().__init__()
        self.term = "고지"
        self.coda = False
        self.food_produce = 1
        self.resistance_power = 2

class UpgradedArea(AriArea):
    # 추상 클래스 (아직 abc 어떻게 쓰는지 모름)

    def __init__(self):
        super().__init__()

    def upgrade_from(self, prev:AriArea):
        self.check_prev(prev)
        for key in prev.__dict__.keys():
            self.__dict__[key] = prev.__dict__[key]
        self.history.append(prev.term)

    def check_prev(prev:AriArea):
        print("false check")

class LowLevelArea(UpgradedArea):

    def __init__(self):
        super().__init__()
        self.level = 1

    def check_prev(self, prev:WildArea):
        if not isinstance(prev, WildArea):
            raise Exception(f"{self.term}의 선행 블럭이 충족되지 않았습니다.")

class Residence(LowLevelArea):
    
    def __init__(self):
        super().__init__()
        self.term = "거주지"
        self.coda = False
        self.supply_produce = 2
        self.power_produce = 3
        self.food_cost = 4
        self.material_cost = 4

class Farm(LowLevelArea):

    def __init__(self):
        super().__init__()
        self.term = "농경지"
        self.coda = False
        self.food_produce = 3
        self.resistance_power = 1
        self.material_cost = 3

class FelledArea(LowLevelArea):
    
    def __init__(self):
        super().__init__()
        self.term = "벌목지"
        self.coda = False
        self.material_produce = 3
        self.resistance_power = 1
        self.food_cost = 3

class Wall(LowLevelArea):

    def __init__(self):
        super().__init__()
        self.term = "방어벽"
        self.resistance_power = 3
        self.food_cost = 5
        self.material_cost = 5

class HighLevelArea(UpgradedArea):

    def __init__(self):
        super().__init__()
        self.level = 3

    def check_prev(self, prev:AriArea):
        if not isinstance(prev, LowLevelArea):
            raise Exception(f"{self.term}의 선행 블럭이 충족되지 않았습니다.")
        elif not isinstance(prev, Residence):
            raise Exception(f"{self.term}의 선행 블럭인 주거지가 충족되지 않았습니다.")

class GovernmentOffice(HighLevelArea):

    def __init__(self):
        super().__init__()
        self.term = "관청"
        self.food_produce = 1
        self.material_produce = 1
        self.supply_produce = 3
        self.resistance_power = 5
        self.food_cost = 10
        self.material_cost = 8
    
class Barrack(HighLevelArea):

    def __init__(self):
        super().__init__()
        self.term = "병영"
        self.food_produce = 1
        self.material_produce = 1
        self.supply_produce = 5
        self.resistance_power = 3
        self.food_cost = 5
        self.material_cost = 5

class ReinforcedWall(HighLevelArea):

    def __init__(self):
        super().__init__()
        self.term = "보강벽"
        self.resistance_power = 8
        self.food_cost = 10
        self.material_cost = 10
    
    def check_prev(self, prev:AriArea):
        if not isinstance(prev, Wall):
            raise Exception(f"{self.term}의 선행 블럭인 방어벽이 충족되지 않았습니다.")


def generate_random_wildarea():
    wildarea = random.choice([Grassland, Plain, Forest, Hill])
    return wildarea()

# 지역 데이터 클래스로 포트 (이 파일이 메인으로 실행되지 않을 때만)
if __name__ != "__main__":
    ari_area: dict[str, AriArea] = dict()
    for k, v in aridatas.area.items():
        ari_area[k] = getattr(modules[__name__], v["classname"])()
        ari_area[k].port(**v)

    ari_military: dict[str, Military] = dict()
    for k, v in aridatas.military.items():
        ari_military[k] = Military()
        ari_military[k].port(**v)