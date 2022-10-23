from AriCont import *

AriS = AriSystem()
AriS.port(**ari_system)

def IDgen(mode="A"): # 간단하게 ID를 만드는 함수
    if "A" in mode:
        return mode + str(AriS.areaseq)
    if "N" in mode:
        return mode + str(AriS.nationseq)

def has_coda(number:str|int):
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

    def __init__(self):
        super().__init__()
        self.ID = ""
        self.birth_stamp = 0  # AriSlena.py에서 지정해야 함

        self.food = Food()
        self.material = Material()
        self.science = Science()
        self.culture = Culture()
        self.gold = Gold()
        self.adminitration_power = AdministrationPower()

    def generate(self):
        # 새로운 객체 생성
        raise Exception("Not Implemented")

    
class AriNation(Manageable):

    def __init__(self):
        super().__init__()
        self.leader = ""  # "닉네임#구별자" 형식

        self.manageable_area_limit = 0
    
    def generate(self):
        # 초기화된 나라 객체에 기본 정보 넣기
        pass
    

class AriArea(Manageable):

    def __init__(self):
        super().__init__()
        self.leader = "" # "닉네임#구별자" 형식
        self.capital = False

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
        self.ID = IDgen("A")
        self.name = "지역 " + str(AriS.areaseq)
        self.owner = "없음"
        self.coda = has_coda(self.ID)
        AriS.areaseq += 1

    def commit(self):
        ari_area[self.ID] = self.whole_info()