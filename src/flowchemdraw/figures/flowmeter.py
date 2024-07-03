import numpy as np
from flowchemdraw.utils.drawclass import components
from flowchemdraw.utils import math
from matplotlib.figure import Figure

PATTERN_DIMENSION = 1
class flowmeter(components):

    type_object = 'devices'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'flowmeter'):

        super().__init__(ax=ax, position=pos, type_object=flowmeter.type_object, name=name, parent=self)

        self.settup_connections()

        self.build()

    def build(self):
        phis = np.arange(0, 6.28, 0.01)
        r = PATTERN_DIMENSION / 2
        self.add_part(self.ax.plot(*math.xy(r, phis, pos=self.position), c='k', ls='-')[0])

        pos = (self.position[0], self.position[1] + 1.5 * r)
        phis = np.arange(-0.73 * np.pi, -0.27 * np.pi, 0.01)
        self.add_part(self.ax.plot(*math.xy(r, phis, pos=pos), c='k', ls='-')[0])

        pos = (self.position[0], self.position[1] - 1.5 * r)
        phis = np.arange(0.27 * np.pi, 0.73 * np.pi, 0.01)
        self.add_part(self.ax.plot(*math.xy(r, phis, pos=pos), c='k', ls='-')[0])


        self._putname_(self.position[0], self.position[1] - 1.5 * r)