import numpy as np
from flowchemdraw.utils.drawclass import components
from flowchemdraw.utils import math
from matplotlib.figure import Figure

class bubblesensor(components):

    type_object = 'devices'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'bubblesensor'):

        super().__init__(ax=ax, position=pos, type_object=bubblesensor.type_object, name=name, parent=self)

        self.settup_connections()

        self.build()

    def build(self):
        phis = np.arange(0, 6.28, 0.01)
        r = self.dimention / 2
        self.add_part(self.ax.plot(*math.xy(r, phis, pos=self.position), c='k', ls='-')[0])

        a = 1 * r / 5

        b = 5/2 * r / 5

        t = np.arange(0, 2 * np.pi, np.pi / 30)

        x = a * (1 - np.sin(t)) * np.cos(t) + self.position[0]
        y = b * (np.sin(t) - 1) + r/2 + self.position[1]

        self.add_part(self.ax.plot(x, y, c='k', ls='-')[0])

        self._putname_(self.position[0], self.position[1] - 1.5 * r)