import importlib

module_name = input("Module: ")
module = importlib.import_module(module_name)
print(module)
