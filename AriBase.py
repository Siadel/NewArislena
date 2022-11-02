from AriExce import *
from typing import *
import json

# json 데이터 저장 함수
# 위에 있는 데이터 저장 함수 이용
# filename 파라미터에 area가 포함되어 있으면
# ./datas/area.json 파일에 저장
# filename 파라미터에 government이 포함되어 있으면
# ./datas/government.json 파일에 저장

def save_json(data: dict, filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# json 데이터 불러오기 함수
def load_json(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

ari_const = load_json("./bases/const.json")

# 지역과 나라를 구성하는 데 쓰이는 것들

# 기타

# 옵션들 (필요할 지는 모르겠음)

class AriOption:

    def __init__(self):
        pass

class AreaOption(AriOption):

    def __init__(self):
        pass

# 기초

class AriBase:

    def __init__(self):
        self.name = ""
        self.coda = True
        self.tradable: bool|None = None # 귀찮으니 알아서 True/False 지정해

    def change_coda(self):
        # self.coda를 반전시킴
        self.coda = not self.coda
    
    def nominative(self):
        # self.coda가 True면 self.name + "이"를 반환
        # False면 self.name + "가"를 반환
        if self.coda:
            return self.name + "이"
        else:
            return self.name + "가"
    
    def objective(self):
        # self.coda가 True면 self.name + "을"를 반환
        # False면 self.name + "를"를 반환
        if self.coda:
            return self.name + "을"
        else:
            return self.name + "를"
    
    def topicmarker(self):
        # self.coda가 True면 self.name + "은"를 반환
        # False면 self.name + "는"를 반환
        if self.coda:
            return self.name + "은"
        else:
            return self.name + "는"


class Value(AriBase):

    def __init__(self):
        super().__init__()
        self.value = 0

    def add_base(self, other):
        if isinstance(other, int):
            self.value += other
        elif type(self) == type(other):
            self.value += other.value
    
    def sub_base(self, other):
        remember = self.value
        if isinstance(other, int):
            self.value -= other
        elif type(self) == type(other):
            self.value -= other.value
        
        if self.value < 0:
            self.value = remember
            raise BelowZero()
    
    def mul_base(self, other):
        if isinstance(other, int):
            self.value *= other
        elif type(self) == type(other):
            self.value *= other.value

    def __add__(self, other):
        self.add_base(other)
    
    def __radd__(self, other):
        self.add_base(other)
    
    def __sub__(self, other):
        self.sub_base(other)
    
    def __rsub__(self, other):
        self.sub_base(other)    
    
    def __mul__(self, other):
        self.mul_base(other)

    def __rmul__(self, other):
        self.mul_base(other)

class OnlyOneClass:

    instance_generated = False

    def __new__(cls):
        if not cls.instance_generated:
            cls.instance_generated = True
            return super().__new__(cls)
        else:
            return None

    def __init__(self):
        pass

# 단계 (추상)
class Level(Value):

    def __init__(self):
        super().__init__()
        self.coda = False
        self.scale: int = 0
    
    def impact(self) -> float:
        return round((1 + self.scale) ** self.value, 4)

class Abundance(Level):

    def __init__(self):
        super().__init__()
        self.scale = 0.25

class Fertility(Abundance):

    def __init__(self):
        super().__init__()
        self.name = "자원 풍요 단계"

class Richness(Abundance):
    
    def __init__(self):
        super().__init__()
        self.name = "자재 풍요 단계"

class Eureka(Abundance):
    
    def __init__(self):
        super().__init__()
        self.name = "과학 풍요 단계"

class Inspiration(Abundance):
    
    def __init__(self):
        super().__init__()
        self.name = "문화 풍요 단계"

# 단계 
class Amenity(Level):

    def __init__(self):
        super().__init__()
        self.name = "쾌적 단계"
        self.scale = 0.1



# 자원
class Resource(Value):

    def __init__(self):
        super().__init__()
        self.tradable = True
        self.has_limitation = True
        self.storage = 0

    def recover(self):
        if self.has_limitation and self.value < self.storage:
            self.value = self.storage
        

    def expire(self):
        # deprecated
        # 저장량을 초과한 자원 제거
        # 단, self.has_limitation이 False면 아무 일도 일어나지 않음
        if self.has_limitation and self.value > self.storage:
            self.value = self.storage


class Food(Resource):

    def __init__(self):
        super().__init__()
        self.name = "식량"

class Material(Resource):

    def __init__(self):
        super().__init__()
        self.name = "자재"
        self.coda = False



# 행정력
class AdministrationPower(Resource):

    def __init__(self):
        super().__init__()
        self.value = 1
        self.name = "행정력"
        self.tradable = False
        self.has_limitation = False
    
    

# 자원분야

class Place(Value):

    def __init__(self):
        # 이 클래스의 .value는 장소에 종사하는 인구수를 나타냄
        super().__init__()
        self.coda = False
        self.tradable = False

class Residence(Place):

    def __init__(self):
        super().__init__()
        self.name = "주거지"
        


class Workplace(Place):

    def __init__(self):
        super().__init__()
        self.food_yield = 0
        self.material_yield = 0
        self.science_yield = 0
        self.culture_yield = 0
        self.gold_yield = 0
        self.administrationpower_yield = 0

        self.food_cost = 0
        self.material_cost = 0
        self.gold_cost = 0
    
    def calc_yield(self):
        pass

class FoodField(Workplace):

    def __init__(self):
        super().__init__()
        self.name = "식량 분야"
        self.food_yield = 3
        self.material_cost = 1

class MaterialField(Workplace):
    
    def __init__(self):
        super().__init__()
        self.name = "자재 분야"
        self.material_yield = 6
        self.food_cost = 1

class ScienceField(Workplace):
    
    def __init__(self):
        super().__init__()
        self.name = "과학 분야"
        self.science_yield = 1
        
        self.food_cost = 1
        self.material_cost = 2

class CultureField(Workplace):
    
    def __init__(self):
        super().__init__()
        self.name = "문화 분야"
        self.culture_yield = 1

        self.food_cost = 2
        self.material_cost = 1

class CommercialField(Workplace):
    
    def __init__(self):
        super().__init__()
        self.name = "상업 분야"
        self.gold_yield = 12

        self.food_cost = 1
        self.material_cost = 1

class AdministrationField(Workplace):

    def __init__(self):
        super().__init__()
        self.name = "행정 분야"
        self.administrationpower_yield = 1

        self.food_cost = 1
        self.material_cost = 1
        self.gold_cost = 4


# 턴

class AriTurn(OnlyOneClass, Value):
    # 단 한 개만 존재하는 클래스
    # 게임의 턴을 관리하는 클래스
    # 턴이 넘어갈 때마다 turn을 1 증가시킴
    # turn이 0이면 게임이 시작되지 않은 상태
    # turn이 60이면 게임이 끝남

    def __init__(self):
        OnlyOneClass.__init__(self)
        Value.__init__(self)
        self.name = "턴"
        self.turn_limit = 60

    def next_turn(self):
        self.value += 1
