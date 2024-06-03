from flowchem.devices.list_known_device_type import _autodiscover_devices_in_module
import flowchem.devices as f
import pkgutil
import importlib
import sys
import tomllib
import re
import inspect


class devices_flowchem:

    def __init__(self):

        self.config_file = None

        self.device_available = _autodiscover_devices_in_module(f)

        self.all_devices_available = self.creat_dict_devices(self.device_available)

        self.devices = self.all_devices_available


    def read_toml_file(self, file):

        self.config_file = file

        with open(file, "rb") as f:
            data = tomllib.load(f)

        lista_toml = [data['device'][name]['type'] for name in data['device'].keys()]
        self.devices = dict()
        for dev in lista_toml:
            if dev in self.device_available.keys():
                self.devices[dev] = self.all_devices_available[dev]
            else:
                print(f'Device {dev} is not found in the flowchem!')


    def found_argument_components(self, lines, argument) -> str:
        line_found_str = f'argument {argument} not found in the script'
        i = 0
        for line in lines:
            if argument in line:
                line_found_str = line.split('=')[1]
                k = 1
                while line_found_str[-1] != ']':
                    line_found_str = line_found_str + lines[i + k]
                    k += 1
                line_found_str = line_found_str.replace(" ", "")
                break
            i += 1

        return f'({line_found_str})'


    def inspect_specific_line(self, cls, method_name, search_text) -> None | str:

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
        lines_found = []
        lines = method_source.split('\n')
        found = False
        i = 0
        for line in lines:
            if search_text in line:
                line_found_str = re.sub('self.components.extend', '', line.strip())
                k = 1
                while line_found_str[-1] != ')':
                    line_found_str = line_found_str + lines[i+k]
                    k += 1

                line_found_str = line_found_str.replace(" ", "")

                if line_found_str[1] != '[':
                    line_found_str = self.found_argument_components(lines, line_found_str[1:-1])

                lines_found.append(line_found_str)
                found = True
            i += 1

        if found:
            return lines_found


    def creat_dict_devices(self, lista: list) -> dict:

        devices = dict()
        for l in lista.keys():
            lin_pakage = self.inspect_specific_line(lista[l], 'initialize', 'self.components.extend')
            if not lin_pakage == None:
                componet = dict()
                for line in lin_pakage:
                    if 'inrange' in line:
                        class_pattern = r'(\w+)\(f"([^"]+)"'
                        class_matches = re.findall(class_pattern, line)
                        repetition_pattern = r'range\((\d+)\)'
                        repetition_matches = re.findall(repetition_pattern, line)
                        # Extract the class name and first argument pattern
                        if class_matches:
                            class_name, first_argument_pattern = class_matches[0]
                        # Extract the number of repetitions
                        if repetition_matches:
                            number_of_repetitions = int(repetition_matches[0])

                        names = [first_argument_pattern.split('{')[0] + str(n+1) for n in range(number_of_repetitions)]
                        for name in names:
                            componet[name] = class_name
                    else:
                        # Find all matches
                        pattern = r'(\w+)\("([^"]+)"'

                        matches = re.findall(pattern, line)

                        # Print the results
                        for match in matches:
                            class_name, first_argument = match
                            componet[first_argument] = class_name

                devices[l] = {'components': componet}
            else:
                devices[l] = {'components': None}

        return devices


