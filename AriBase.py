from AriExce import *
# 지역과 나라를 구성하는 데 쓰이는 것들

# 기초 (추상)

class Tradable:

    def __init__(self):
        self.tradable = True

class Untradable:

    def __init__(self):
        self.tradable = False

class Valuable:

    def __init__(self, value):
        self.value = value

    def add_base(self, other):
        if isinstance(other, int):
            self.value += other
        elif type(self) == type(other):
            self.value += other.value
    
    def sub_base(self, other):
        remember = self.value
        if isinstance(other, int):
            self.value -= other
        elif type(self) == type(other):
            self.value -= other.value
        
        if self.value < 0:
            self.value = remember
            raise BelowZero()
    
    def mul_base(self, other):
        if isinstance(other, int):
            self.value *= other
        elif type(self) == type(other):
            self.value *= other.value

    def __add__(self, other):
        self.add_base(other)
    
    def __radd__(self, other):
        self.add_base(other)
    
    def __sub__(self, other):
        self.sub_base(other)
    
    def __rsub__(self, other):
        self.sub_base(other)    
    
    def __mul__(self, other):
        self.mul_base(other)

    def __rmul__(self, other):
        self.mul_base(other)



# 단계 (추상)
class Level(Valuable, Untradable):

    def __init__(self, value):
        Valuable.__init__(self, value)
        Untradable.__init__(self)
        self.scale: int = 0
    
    def impact(self):
        return round((1 + self.scale) ** self.value, 4)

class Abundance(Level):

    def __init__(self, value):
        super().__init__(value)
        self.scale = 0.25

# 단계 
class Amenity(Level):

    def __init__(self, value):
        super().__init__(value)
        self.scale = 0.1

class Fertility(Abundance):

    def __init__(self, value):
        super().__init__(value)

class Richness(Abundance):

    def __init__(self, value):
        super().__init__(value)

# 전략 (추상)
class Strategy:

    def __init__(self):
        pass

# 전략
class DefaultStrategy(Strategy):

    def __init__(self):
        super().__init__()

# 자원 (추상)
class Resource(Valuable, Tradable):

    def __init__(self, value):
        Valuable.__init__(self, value)
        Tradable.__init__(self)        

class Storable(Resource):

    def __init__(self, value):
        super().__init__(value)

    @staticmethod
    def storelimit(initial=100):
        return initial

    def expire(self):
        # 저장량을 초과한 자원 제거
        storelimit = self.storelimit()
        if self.value > storelimit:
            self.value = storelimit

# 자원
class Food(Storable):

    def __init__(self, value):
        super().__init__(value)

class Material(Storable):

    def __init__(self, value):
        super().__init__(value)

class Science(Resource):

    def __init__(self, value):
        super().__init__(value)

class Culture(Resource):

    def __init__(self, value):
        super().__init__(value)

class Gold(Resource):

    def __init__(self, value):
        super().__init__(value)

# 행정력
class AdministrationPower(Resource):

    def __init__(self, value):
        super().__init__(value)
        self.accomodatable_population = 3

# 인구 (추상)
class Population(Resource):

    def __init__(self, value):
        super().__init__(value)
        self.humanpower = 0
        
        self.food_cost = 0
        self.material_cost = 0
        self.gold_cost = 0

        self.food_yield = 0
        self.material_yield = 0
        self.science_yield = 0
        self.culture_yield = 0
        self.gold_yield = 0

# 인구
class Labor(Population):

    def __init__(self, value):
        super().__init__(value)
        self.humanpower = 3

class Worker(Labor):

    def __init__(self, value):
        super().__init__(value)
        self.humanpower = 2
        self.modifier = 3

class Administrative(Population):

    def __init__(self, value):
        super().__init__(value)
        self.humanpower = 1
        self.food_cost = 2
        self.material_cost = 2

class Military(Population):

    def __init__(self, value):
        super().__init__(value)
        self.humanpower = 1
        self.food_cost = 2
        self.material_cost = 4


# TODO: 분야 다시 짜야 함
# 분야 (추상)
class Field:

    def __init__(self):
        pass
    
    def calc_yield(self):
        pass

# 자원분야(추상)

class ResourceField(Field):

    def __init__(self, labors:Labor, workers:Worker):
        super().__init__()
        self.labors = labors
        self.workers = workers

class FoodField(ResourceField):

    def __init__(self, labors:Labor, workers:Worker):
        super().__init__(labors, workers)
        self.labors.food_yield = 1
        self.workers.food_yield = 3

        self.workers.material_cost = 1

class MaterialField(ResourceField):
    
    def __init__(self, labors:Labor, workers:Worker):
        super().__init__(labors, workers)
        self.labors.material_yield = 1
        self.workers.material_yield

        self.workers.food_cost = 1

class ScienceField(ResourceField):
    
    def __init__(self, labors:Labor, workers:Worker):
        super().__init__(labors, workers)
        self.workers.food_cost = 1
        self.workers.material_cost = 2

class CultureField(ResourceField):
    
    def __init__(self, labors:Labor, workers:Worker):
        super().__init__(labors, workers)
        self.workers.food_cost = 2
        self.workers.material_cost = 1

class CommercialField(ResourceField):
    
    def __init__(self, labors:Labor, workers:Worker):
        super().__init__(labors, workers)

class AdministrationField(Field):

    def __init__(self, administratives:Administrative):
        super().__init__()
        self.administratives = administratives

class MilitaryField(Field):

    def __init__(self, military:Military):
        super().__init__()
        self.military = military