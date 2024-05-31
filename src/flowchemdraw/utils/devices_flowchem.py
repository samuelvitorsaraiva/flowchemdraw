import pkgutil
import importlib
import sys
import tomllib

def flowchem_devices() -> list:

    all_classes = []

    # Import the top-level package
    package = importlib.import_module("flowchem.devices")

    # Iterate through all submodules in the package
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
        module = importlib.import_module(modname)

        # Extract the __all__ variable
        if hasattr(module, "__all__"):
            all_classes.extend(getattr(module, "__all__"))

    return all_classes


def read_toml_file(name):

    from flowchem.server.configuration_parser import parse_config, instantiate_device_from_config

    with open(name, "rb") as f:
        data = tomllib.load(f)

    devices = instantiate_device_from_config(data)

    return data


import inspect


def inspect_specific_line(cls, method_name, search_text):
    # Get the method object
    method = getattr(cls, method_name, None)

    if method is None:
        print(f"Method '{method_name}' not found in class '{cls.__name__}'.")
        return

    # Get the source code of the method
    try:
        method_source = inspect.getsource(method)
    except TypeError:
        print(f"Could not retrieve source code for method '{method_name}'.")
        return

    # Search for the specific line
    lines = method_source.split('\n')
    found = False
    for line in lines:
        if search_text in line:
            print(f"Found line: {line.strip()}")
            found = True

    if not found:
        print(f"No line containing '{search_text}' found in method '{method_name}'.")


if __name__ == '__main__':
    from flowchem.devices.list_known_device_type import _autodiscover_devices_in_module
    import flowchem.devices as f
    list = _autodiscover_devices_in_module(f)
    for l in list.keys():
        print(l)
        inspect_specific_line(list[l], 'initialize', 'self.components.extend')
        print('')