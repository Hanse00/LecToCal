import importlib
import inspect

from cakes.cake import Cake


def find_cakes(module):
    cakes = []
    for klass in dir(module):
        attribute = getattr(module, klass)
        if (inspect.isclass(attribute) and issubclass(attribute, Cake) and 
        attribute != Cake):
            cakes.append(attribute)
    return cakes


#module_name = input("Which cake? ")
module_name = "cakes.brownie"
module = importlib.import_module(module_name)
print(module)
print(find_cakes(module))
