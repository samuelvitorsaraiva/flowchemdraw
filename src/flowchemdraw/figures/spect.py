import numpy as np
from flowchemdraw.utils.drawclass import components
from matplotlib.figure import Figure
from flowchemdraw.utils import math

class spect(components):

    type_object = 'devices'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'spect'):

        super().__init__(ax=ax, position=pos, type_object=spect.type_object, name=name, parent=self)

        self.build()

    def build(self):
        phis = np.arange(0, 6.28, 0.01)
        r = self.dimention / 2
        self.add_part(self.ax.plot(*math.xy(r, phis, pos=self.position), c='k', ls='-')[0])

        x = np.linspace(self.position[0] - r, self.position[0] + r, 100)
        arg = r / 2 * np.sin(2 * np.pi * (x - x[0]) / (x[-1] - x[0])) + self.position[1]
        self.add_part(self.ax.plot(x, arg, color='k')[0])

        self._putname_(self.position[0], self.position[1] - 1.5 * r)

        self.connection_points = [(self.position[0] - r, self.position[1]), (self.position[0] + r, self.position[1])]