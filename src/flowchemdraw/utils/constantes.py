SPACE_GRID_FIG = 20

PATTERN_DIMENSION = 1

MIN_DISTANCE_TO_ACTIVATED = 1

MIN_DISTANCE_TO_MOVE = 1

LOCATION_NEW_DEVICES = (SPACE_GRID_FIG - MIN_DISTANCE_TO_ACTIVATED, SPACE_GRID_FIG - MIN_DISTANCE_TO_ACTIVATED)

ITENS_GROUPS = 'devices connections others'.split()

COMPONENTS_NONELETRONIC = ['erlenmeyer', 'flowreactor']

DRAW_DEVICES_CORRESPONDENT = {
    'AzuraCompact/pump': 'pump',
    'Elite11': 'syringe',
    'ML600/pump': 'pump',
    'ML600/pump': 'left_pump',
    'ML600/pump': 'right_pump',
    'ML600/valve': 'valve',
    'ML600/valve': 'left_valve',
    'ML600/valve': 'right_valve',
    'plugins/pump': 'pump',
    'plugins/valve': 'pump'
}