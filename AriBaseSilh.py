from base import *
import json

# AriBase 파일 클래스 작동 실험
# 클래스 선언이 아닌 클래스 사용 코드

food = Food(100)
matl = Material(50)

print(f"현재 {food.topicmarker()} {food.value}이고, 저장량은 {food.storage}입니다.")
print(f"현재 {matl.topicmarker()} {matl.value}이고, 저장량은 {matl.storage}입니다.")

# 실험용 json 파일 "silh.json"을 만들고, 그 안에 food와 matl의 정보를 __dict__ 메소드를 이용해서 저장

with open("silh.json", "w", encoding="utf-8") as file:
    di = {"food": food.__dict__, "matl": matl.__dict__}
    json.dump(di, file, ensure_ascii=False, indent=4)

# 새로운 변수 food2와 matl2를 만들고, silh.json 파일에서 정보를 불러와서 food2와 matl2에 저장하는데
# food2와 matl2는 각각 Food와 Material 클래스여야 함


with open("silh.json", "r", encoding="utf-8") as file:
    di = json.load(file)
food2 = Food()
matl2 = Material()
food2.__dict__ = di["food"]
matl2.__dict__ = di["matl"]

print(food2.__dict__, matl2.__dict__)