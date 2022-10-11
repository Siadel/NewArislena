from AriExce import *
# 지역과 나라를 구성하는 데 쓰이는 것들

# 자원
class Resource:

    def __init__(self):
        self.quantity:int = 0

    def __add__(self, other:int):
        self.quantity += other
    
    def __sub__(self, other:int):
        self.quantity -= other
    
    def __mul__(self, other:int):
        self.quantity *= other

class StoreResource(Resource):

    def __init__(self):
        super().__init__()
        self.storelimit = 0

    def __add__(self, other: int):
        if self.quantity + other > self.storelimit:
            raise OverTheLimit()
        else:
            super().__add__(other)
    
    def __sub__(self, other: int):
        if self.quantity - other < self.storelimit:
            raise BelowZero()
        else:
            super().__add__(other)

class BasicResource(StoreResource):

    def __init__(self):
        super().__init__()
        self.storelimit:int = 100

class DevelopmentalResource(Resource):

    def __init__(self):
        super().__init__()

class AdvancedResource(Resource):

    def __init__(self):
        super().__init__()


class Food(BasicResource):

    def __init__(self):
        super().__init__()

class Material(BasicResource):

    def __init__(self):
        super().__init__()

class Tech(DevelopmentalResource):

    def __init__(self):
        super().__init__()

class Culture(DevelopmentalResource):

    def __init__(self):
        super().__init__()

class Gold(AdvancedResource):

    def __init__(self):
        super().__init__()

class Faith(AdvancedResource):

    def __init__(self):
        super().__init__()

class Power(Resource):

    def __init__(self):
        super().__init__()


# 스탯
class Stat:

    def __init__(self):
        self.quantity = 0
        self.food_consumption = 0
        self.material_consumption = 0
        self.gold_consumption = 0
        self.yld = 0

class BasicResourceStat(Stat):

    def __init__(self):
        super().__init__()

class DevelopmentalResourceStat(Stat):

    def __init__(self):
        super().__init__()

class AdvancedResourseStat(Stat):

    def __init__(self):
        super().__init__()


class FoodStat(BasicResourceStat):

    def __init__(self):
        super().__init__()
        self.material_consumption = 1
        self.yld = 2

class MaterialStat(BasicResourceStat):

    def __init__(self):
        super().__init__()
        self.food_consumption = 1
        self.yld = 4

class TechStat(DevelopmentalResourceStat):

    def __init__(self):
        super().__init__()
        self.food_consumption = 1
        self.material_consumption = 2
        self.gold_consumption = 2
        self.yld = 1
    
class CultureStat(DevelopmentalResourceStat):

    def __init__(self):
        super().__init__()
        self.food_consumption = 2
        self.material_consumption = 1
        self.gold_consumption = 2
        self.yld = 1

class CommercialStat(AdvancedResourseStat):

    def __init__(self):
        super().__init__()
        self.food_consumption = 1
        self.material_consumption = 1
        self.yld = 16

class FaithStat(AdvancedResourseStat):

    def __init__(self):
        super().__init__()
        self.food_consumption = 1
        self.material_consumption = 1
        self.yld = 8

class PowerStat(Stat):

    def __init__(self):
        super().__init__()
        self.food_consumption = 1
        self.material_consumption = 2
        self.gold_consumption = 3
