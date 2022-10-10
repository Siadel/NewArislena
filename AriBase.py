# 지역과 나라를 구성하는 데 쓰이는 것들

# 자원
class Resource:

    def __init__(self, amount:int):
        self.amount = amount

    def __add__(self, other:int):
        self.amount += other
    
    def __sub__(self, other:int):
        self.amount -= other
    
    def __mul__(self, other:int):
        self.amount *= other

class StoreResource(Resource):

    def __init__(self, amount:int, storage:int):
        super().__init__(amount)
        self.storage:int = storage

    def __add__(self, other: int):
        predict = self.amount + other
        if predict > self.storage:
            self.amount = predict
        else:
            super().__add__(other)
    
    def __sub__(self, other: int):
        predict = self.amount - other
        if predict < self.storage:
            self.amount = 0
        else:
            super().__add__(other)

class BasicResource(StoreResource):

    initial_storage = 100

    def __init__(self, amount:int, storage:int):
        super().__init__(amount)
        self.storage:int = storage

class DevelopmentalResource(Resource):

    def __init__(self, amount:int):
        super().__init__(amount)

class AdvancedResource(StoreResource):

    def __init__(self, amount:int):
        super().__init__(amount)


class Food(BasicResource):

    def __init__(self, amount:int, storage:int):
        super().__init__(amount, storage)

class Material(BasicResource):

    def __init__(self, amount:int, storage:int):
        super().__init__(amount, storage)

class Tech(DevelopmentalResource):

    def __init__(self, amount:int):
        super().__init__(amount)

class Culture(DevelopmentalResource):

    def __init__(self, amount:int):
        super().__init__(amount)

class Gold(AdvancedResource):

    def __init__(self, amount:int):
        super().__init__(amount)

class Faith(AdvancedResource):

    def __init__(self, amount:int):
        super().__init__(amount)


# 스탯
class Stat:

    def __init__(self, amount:int):
        self.amount = amount
    

class BasicResourceStat(Stat):

    def __init__(self, amount:int):
        super().__init__(amount)

class DevelopmentalResourceStat(Stat):

    def __init__(self, amount:int):
        super().__init__(amount)

class AdvancedResourseStat(Stat):

    def __init__(self, amount:int):
        super().__init__(amount)


class FoodStat(BasicResourceStat):

    initial_material_consumption = 1
    initial_production = 2

    def __init__(self, amount:int):
        super().__init__(amount)

class MaterialStat(BasicResourceStat):

    initial_food_consumption = 1
    initial_production = 4

    def __init__(self, amount:int):
        super().__init__(amount)

class TechStat(DevelopmentalResourceStat):

    initial_food_consumption = 1
    initial_material_consumption = 2

    def __init__(self, amount:int):
        super().__init__(amount)
    
class CultureStat(DevelopmentalResourceStat):

    initial_food_consumption = 2
    initial_material_consumption = 1

    def __init__(self, amount:int):
        super().__init__(amount)

class CommercialStat(AdvancedResourseStat):

    initial_food_consumption = 1
    initial_material_consumption = 1

    def __init__(self, amount:int):
        super().__init__(amount)


