from prod import *

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