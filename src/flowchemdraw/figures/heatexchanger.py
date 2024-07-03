import numpy as np
from flowchemdraw.utils.drawclass import components
from flowchemdraw.utils import math
from matplotlib.figure import Figure

PATTERN_DIMENSION = 1
class heatexchanger(components):

    type_object = 'devices'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'heatexchanger'):

        super().__init__(ax=ax, position=pos, type_object=heatexchanger.type_object, name=name, parent=self)

        self.settup_connections()

        self.build()

    def settup_connections(self):
        self.connection_points = {1: {'name': None, 'pairs': [1], 'position': (self.position[0], self.position[1])}}

    def build(self):
        phis = np.arange(0, 6.28, 0.01)
        r = PATTERN_DIMENSION / 2
        self.add_part(self.ax.plot(*math.xy(r, phis, pos=self.position), c='k', ls='-')[0])


        x = np.linspace(0, 2 * r, 10)
        y = np.round(np.sin(25*x)) * r/3 + self.position[1]
        y[-1] = self.position[1]

        self.add_part(self.ax.plot(x+self.position[0]-r, y, color='k')[0])

        self._putname_(self.position[0], self.position[1] - 1.5 * r)