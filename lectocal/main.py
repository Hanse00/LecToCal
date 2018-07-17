import importlib
import inspect

from cakes.cake import Cake


def find_cakes(module):
    cakes = []
    for name in dir(module):
        attribute = getattr(module, name)
        if (inspect.isclass(attribute) and issubclass(attribute, Cake) and 
        attribute != Cake):
            cakes.append(attribute())
    return cakes


module_name = input("Which cake? ")
module = importlib.import_module(module_name)
print("Module: " + str(module))
cakes = find_cakes(module)
print("Cakes in module: " + str(cakes))
for cake in cakes:
    print(cake.get_name() + " tastes: " + cake.get_taste())
