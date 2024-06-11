SPACE_GRID_FIG = 20

PATTERN_DIMENSION = 1

MIN_DISTANCE_TO_ACTIVATED = 1

MIN_DISTANCE_TO_MOVE = 1

LOCATION_NEW_DEVICES = (SPACE_GRID_FIG - MIN_DISTANCE_TO_ACTIVATED, SPACE_GRID_FIG - MIN_DISTANCE_TO_ACTIVATED)

ITENS_GROUPS = 'devices connections others'.split()

COMPONENTS_NONELETRONIC = ['erlenmeyer', 'flowreactor', 'Tverbinder', 'Xverbinder']

DRAW_DEVICES_CORRESPONDENT = {
'AzuraCompact/pump': 'pump',
'AzuraCompact/pressure': 'sensor',
'CVC3000': 'undefined',
'Clarity': 'chromatography',
'EPC': 'undefined',
'Elite11': 'syringe',
'HuberChiller': 'undefined',
'IcIR': 'spect',
'KnauerDAD/channel1': 'undefined',
'KnauerDAD/channel2': 'undefined',
'KnauerDAD/channel3': 'undefined',
'KnauerDAD/channel4': 'undefined',
'KnauerValve': 'valve',
'MFC': 'undefined',
'ML600/left_pump': 'pump',
'ML600/right_pump': 'pump',
'ML600/pump': 'pump',
'ML600/left_valve': 'valve',
'ML600/right_valve': 'valve',
'ML600/valve': 'valve',
'MansonPowerSupply': 'undefined',
'PhidgetBubbleSensor': 'undefined',
'PhidgetPowerSource5V': 'undefined',
'PhidgetPressureSensor': 'undefined',
'R2/Power': 'undefined',
'R2/PressureSensor': 'undefined',
'R2/GSensor': 'undefined',
'R2/PhotoReactor': 'undefined',
'R2/Pump_A': 'undefined',
'R2/Pump_B': 'undefined',
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
'Spinsolve': 'undefined',
'ViciValve': 'valve',
'plugins/pump1': 'pump',
'plugins/pump2': 'pump',
'plugins/pump3': 'pump',
'plugins/pump4': 'pump',
'plugins/valve': 'valve'
}