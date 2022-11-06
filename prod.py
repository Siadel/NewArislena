from AriSystem import *

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





