from flowchem.devices.list_known_device_type import _autodiscover_devices_in_module
import flowchem.devices as flowchem_dev
from flowchemdraw.utils.manage_class import get_parameters_details
from flowchemdraw.utils.devices_flowchem import creat_dict_devices
import os


SPACE_GRID_FIG = 20

PATTERN_DIMENSION = 1

MIN_DISTANCE_TO_ACTIVATED = 1

MIN_DISTANCE_TO_MOVE = 1

LOCATION_NEW_DEVICES = (SPACE_GRID_FIG - MIN_DISTANCE_TO_ACTIVATED, SPACE_GRID_FIG - MIN_DISTANCE_TO_ACTIVATED)

ITENS_GROUPS = 'devices connections others'.split()

COMPONENTS_NONELETRONIC = ['erlenmeyer', 'flowreactor', 'Tverbinder', 'Xverbinder']

ADRESS = os.path.dirname(os.path.abspath(__file__))[:-6]

DRAW_DEVICES_CORRESPONDENT = {
'AzuraCompact/pump': 'pump',
'AzuraCompact/pressure': 'pressure_sensor',
'CVC3000': 'pressure_sensor',
'Clarity': 'chromatography',
'EPC': 'flowmeter',
'Elite11': 'syringe',
'HuberChiller': 'heatexchanger',
'IcIR': 'spect',
'KnauerDAD/channel1': 'undefined',
'KnauerDAD/channel2': 'undefined',
'KnauerDAD/channel3': 'undefined',
'KnauerDAD/channel4': 'undefined',
'KnauerValve': 'valve',
'MFC': 'flowmeter',
'ML600/left_pump': 'pump',
'ML600/right_pump': 'pump',
'ML600/pump': 'pump',
'ML600/left_valve': 'valve',
'ML600/right_valve': 'valve',
'ML600/valve': 'valve',
'MansonPowerSupply': 'undefined',
'PhidgetBubbleSensor': 'bubblesensor',
'PhidgetPowerSource5V': 'undefined',
'PhidgetPressureSensor': 'pressure_sensor',
'R2/Power': 'undefined',
'R2/PressureSensor': 'pressure_sensor',
'R2/GSensor': 'undefined',
'R2/PhotoReactor': 'undefined',
'R2/Pump_A': 'pump',
'R2/Pump_B': 'pump',
'R2/ReagentValve_A': 'undefined',
'R2/ReagentValve_B': 'undefined',
'R2/CollectionValve': 'undefined',
'R2/InjectionValve_A': 'undefined',
'R2/InjectionValve_B': 'undefined',
'R2/PumpSensor_A': 'undefined',
'R2/PumpSensor_B': 'undefined',
'R2/Reactor-1': 'undefined',
'R2/Reactor-2': 'undefined',
'R2/Reactor-3': 'undefined',
'R2/Reactor-4': 'undefined',
'R4Heater/reactor1': 'undefined',
'R4Heater/reactor2': 'undefined',
'R4Heater/reactor3': 'undefined',
'R4Heater/reactor4': 'undefined',
'Spinsolve': 'spect',
'ViciValve': 'valve',
'plugins/pump1': 'pump',
'plugins/pump2': 'pump',
'plugins/pump3': 'pump',
'plugins/pump4': 'pump',
'plugins/valve': 'valve'
}

CLASS_DEVICE_AVAILABLE_FLOWCHEM = _autodiscover_devices_in_module(flowchem_dev)

CONFIGURATION_FILE_COMPLETE = {'device': dict()}
for dev in CLASS_DEVICE_AVAILABLE_FLOWCHEM.keys():
    # Get constructor arguments
    CONFIGURATION_FILE_COMPLETE['device'][dev] = get_parameters_details(CLASS_DEVICE_AVAILABLE_FLOWCHEM[dev].__init__)

CLASS_COMPONENT_DEVICE_AVAILABLE_FLOWCHEM = creat_dict_devices(CLASS_DEVICE_AVAILABLE_FLOWCHEM)
