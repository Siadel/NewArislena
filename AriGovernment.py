from AriProduceable import *

class AriGovernment(Manageable):

    data = aridatas.government

    def __init__(self):
        super().__init__()
        self.leader: str|None = None  # "닉네임#구별자" 형식
        self.settle_point = 0 # 사용 가능한 정착 포인트
        self.victory_point = 0 # 승리 포인트

        self.food = Food()
        self.material = Material()
        self.administration_power = 0

        self.supply_limit = 0 # 사용 가능한 최대 군사
    
    def generate(self, *, name:str|None=None, leader:str|None=None, coda:bool=True):
        # 초기화된 지도부 객체에 기본 정보 넣기
        self.ID = ari_system.IDgen("G")
        self.name = "지도부 " + str(ari_system.areaseq) if name is None else name
        self.leader = leader
        self.coda = has_coda(self.name) if coda is None and name is None else coda
        ari_system.areaseq += 1
    
    def get_every_manageable_militaries(self):
        # 지도부가 관리할 수 있는 군사들의 정보를 반환
        return [military for military in ari_military.values() if military.dominator == self.ID]

    def get_every_dominating_areas(self):
        # 지도부가 지배하는 지역들의 정보를 반환
        return [area for area in ari_area.values() if area.dominator == self.ID]

    def calc_supply_point(self):
        rtn = 0
        for area in self.get_every_dominating_areas():
            rtn += area.supply_produce
        return rtn

    def calc_administration_power(self):
        # 행정력 계산
        pass

    def calc_accomodatable_area(self):
        if self.value == 0:
            return 7
        elif self.value == 1:
            return 11
        elif self.value == 2:
            return 13
    
    def end_of_turn(self):
        # 턴이 끝날 때마다 실행되어야 함
        self.settle_point += 1
    
    

# 지도부 데이터 클래스로 포트
ari_government: dict[str, AriGovernment] = dict()
for k, v in aridatas.government.items():
    ari_government[k] = AriGovernment()
    ari_government[k].port(**v)