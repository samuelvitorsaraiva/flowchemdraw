import importlib

def import_class(module_name, class_name):
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except ModuleNotFoundError:
        print(f"Module {module_name} not found.")
        return None
    except AttributeError:
        print(f"Class {class_name} not found in module {module_name}.")
        return None