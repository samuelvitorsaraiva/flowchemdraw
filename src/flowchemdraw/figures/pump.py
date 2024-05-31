import numpy as np
from flowchemdraw.utils.drawclass import components
from flowchemdraw.utils import math
from matplotlib.figure import Figure

PATTERN_DIMENSION = 1
class pump(components):

    type_object = 'devices'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'pump'):

        super().__init__(ax=ax, position=pos, type_object=pump.type_object, name=name, parent=self)

        self.build()

    def build(self):
        phis = np.arange(0, 6.28, 0.01)
        r = PATTERN_DIMENSION / 2
        self.add_part(self.ax.plot(*math.xy(r, phis, pos=self.position), c='k', ls='-')[0])
        self.add_part(
            self.ax.plot([self.position[0], self.position[0] + r], [self.position[1] - r, self.position[1]], color='k')[0])
        self.add_part(
            self.ax.plot([self.position[0], self.position[0] + r], [self.position[1] + r, self.position[1]], color='k')[0])

        self._putname_(self.position[0], self.position[1] - 1.5 * r)

        self.connection_points = [(self.position[0] - r, self.position[1]), (self.position[0] + r, self.position[1])]