from .cake import Cake

class Layercake(Cake):
    @staticmethod
    def get_name():
        return "Layercake"

    @staticmethod
    def get_taste():
        return "like layers of sweetness."
