from prod import *

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
