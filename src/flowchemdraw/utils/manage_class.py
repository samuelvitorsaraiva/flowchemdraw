import importlib
import inspect

def import_class(module_name: str, class_name: str):
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except ModuleNotFoundError:
        #print(f"Module {module_name} not found.")
        return None
    except AttributeError:
        #print(f"Class {class_name} not found in module {module_name}.")
        return None


def get_package_directory(package_name):
    # Import the package
    package = importlib.import_module(package_name)

    # Get the file path of the package
    package_dir = inspect.getfile(package)

    # Return the directory
    return package_dir


def get_parameters_details(method):
    signature = inspect.signature(method)
    return {
        name: param.default if param.default is not param.empty else None
        for name, param in signature.parameters.items() if name != 'self' and name != 'kwargs' and name != 'name'
    }