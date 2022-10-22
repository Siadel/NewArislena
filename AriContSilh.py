# AriCont.py 모듈을 와일드카드 임포트해서 실험하는 파일

from AriCont import *
from pprint import pprint

#save_json({}, "area")

#silharea:AriArea = AriArea()
#silharea.generate()
#silharea.name = "실버헤이지"
#silharea.capital = True
#silharea.commit()
#pprint(whole_area, indent=4, sort_dicts=False)
#save_json(whole_area, "area")

#whole_area_data = dict()
#for k, v in whole_area.items():
#    whole_area_data[k] = AriArea()
#    whole_area_data[k].port(**v)
#
#pprint(whole_area_data, indent=4, sort_dicts=False)

turn = AriTurn()
turn2 = AriTurn()

print(type(turn), turn.__dict__)
# 출력: <class 'AriCont.AriTurn'> {'name': '턴', 'coda': True, 'tradable': True, 'commit_data': {}, 'turn': 0, 'turn_limit': 60}
print(type(turn2), turn2.__dict__) # 여기서 오류가 뜸: NoneType은 __dict__를 가지지 않음