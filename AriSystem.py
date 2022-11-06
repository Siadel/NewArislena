from content import *

class AriSystem(AriContent, OnlyOneClass):
    # dict로 옮겨진 json 데이터를 관리하는 클래스

    def __init__(self):
        AriContent.__init__(self)
        OnlyOneClass.__init__(self)
        self.name = "아리슬레나"
        self.coda = False
        self.season_version = 0
        self.major_version = 2
        self.minor_version = 11
        self.author = "Siadel#7457"
        self.areaseq = 0
        self.governmentseq = 0
        self.militaryseq = 0
        self.turn = AriTurn()

        

    def IDgen(self, mode:str): # 간단하게 ID를 만드는 함수
        if "A" in mode:
            return mode + str(self.areaseq)
        if "G" in mode:
            return mode + str(self.governmentseq)
        if "M" in mode:
            return mode + str(self.militaryseq)
    
    def version(self):
        return f"{self.season_version}.{self.major_version}.{self.minor_version}"

    def commit(self):
        for k, v in self.whole_info().items():
            aridatas.system[k] = v

# 지역, 군사 데이터 클래스로 포트
ari_area = dict()
for k, v in aridatas.area.items():
    ari_area[k] = getattr(modules[__name__], v["classname"])()
    ari_area[k].port(**v)

ari_military = dict()
for k, v in aridatas.military.items():
    ari_military[k] = getattr(modules[__name__], v["classname"])()
    ari_military[k].port(**v)

aridatas = AriDataFiles()
ari_system = AriSystem()
ari_system.port(**aridatas.system)