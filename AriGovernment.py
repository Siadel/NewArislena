from AriMilitary import *
from AriArea import *



class AriGovernment(Manageable):

    data = aridatas.government

    def __init__(self):
        super().__init__()
        self.leader: str|None = None  # "닉네임#구별자" 형식
        self.settle_point = 1 # 사용 가능한 정착 포인트
        self.victory_point = 0 # 승리 포인트

        self.food = Food()
        self.material = Material()
        self.administration_power = AdministrationPower()

        self.supply_limit = 0 # 사용 가능한 최대 군사
    
    def generate(self, *, name:str|None=None, leader:str|None=None, coda:bool=True):
        # 초기화된 지도부 객체에 기본 정보 넣기
        self.ID = ari_system.IDgen("G")
        self.name = "지도부 " + str(ari_system.governmentseq) if name is None else name
        self.leader = leader
        self.coda = has_coda(self.name) if coda is None and name is None else coda
        ari_system.governmentseq += 1
        ari_government[self.ID] = self
        self.commit()
        ari_system.commit()
    
    def get_every_manageable_militaries(self):
        # 지도부가 관리할 수 있는 군사들의 정보를 반환
        return [military for military in ari_military.values() if military.dominator == self.ID]

    def get_every_dominating_areas(self):
        # 지도부가 지배하는 지역들의 정보를 반환
        return [area for area in ari_area.values() if area.dominator == self.ID]
    
    def get_dominating_area(self, *, name:str|None=None, ID:str|None=None):
        if name is None and ID is None:
            raise ValueError("지역 이름과 ID를 모두 입력하지 않았습니다.")
        for area in self.get_every_dominating_areas():
            if name is not None and area.name == name:
                return area
            elif ID is not None and area.ID == ID:
                return area

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
    
    def upgrade_area(self, target_classname:str, *, name:str|None=None, ID:str|None=None):
        temp = self.get_dominating_area(name=name, ID=ID)
        AID = temp.ID
        target:UpgradedArea = getattr(modules[__name__], target_classname)()
        target.upgrade_from(temp)
        ari_area[AID] = target
        target.commit()

    def settle(self):
        # 새로운 지역을 만들고 자신의 것으로 만듦
        if self.settle_point == 0:
            raise ValueError("정착 포인트가 부족합니다.")
        self.settle_point -= 1
        new_area = generate_random_wildarea()
        new_area.generate(dominator=self.ID)
        new_area.commit()
    

# 지도부 데이터 클래스로 포트
ari_government: dict[str, AriGovernment] = dict()
for k, v in aridatas.government.items():
    ari_government[k] = AriGovernment()
    ari_government[k].port(**v)