import numpy as np
from flowchemdraw.utils.drawclass import components
from flowchemdraw.utils import math
from matplotlib.figure import Figure

class pressure_sensor(components):

    type_object = 'devices'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'pressure_sensor'):

        super().__init__(ax=ax, position=pos, type_object=pressure_sensor.type_object, name=name, parent=self)

        self.connection_central = True

        self.build()

    def build(self):

        phis = np.arange(0, 2 * np.pi, 0.01)
        r = self.dimention
        self.add_part(self.ax.plot(*math.xy(r, phis, pos=self.position), c='k', ls='-')[0])

        self.add_part(self.ax.plot(*math.xy(r/8, phis, pos=self.position), c='k', ls='-')[0])

        n = 10
        phis = np.linspace(- np.pi / 4, (2 + 1 / 2) * np.pi / 2, n)
        x1, y1 = math.xy(r/1.1, phis, pos=self.position)
        x2, y2 = math.xy(r/1.3, phis, pos=self.position)
        for i in range(n):
            self.add_part(self.ax.plot([x1[i], x2[i]], [y1[i], y2[i]], '-', c='k')[0])

        i = np.random.randint(n, size=(1))[0]
        self.add_part(self.ax.plot([self.position[0], x1[i] - r/20], [self.position[1], y1[i] - r/20], c='k', ls='-')[0])

        self._putname_(self.position[0], self.position[1] - 1.5 * r)


        self.connection_points = [(self.position[0] - r, self.position[1]), (self.position[0] + r, self.position[1])]