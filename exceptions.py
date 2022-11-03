
class OverTheLimit(Exception):
    def __init__(self):
        super().__init__("상한을 초과할 수 없어요.")

class BelowZero(Exception):
    def __init__(self) -> None:
        super().__init__("0 미만이 될 수 없어요.")