import numpy as np
from flowchemdraw.utils.drawclass import components
from flowchemdraw.utils import math
from matplotlib.figure import Figure

class valve(components):

    type_object = 'devices'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'valve'):

        super().__init__(ax=ax, position=pos, type_object=valve.type_object, name=name, parent=self)

        self.connections = 6

        self.connection_central = True

        self.build()

    def build(self):

        phis = np.arange(0, 2 * np.pi, 0.01)
        r = self.dimention
        self.add_part(self.ax.plot(*math.xy(r, phis, pos=self.position), c='k', ls='-')[0])

        phis = np.linspace(np.pi / 4, (2 + 1 / 4) * np.pi, self.connections + 1)
        r = self.dimention / 1.3
        x, y = math.xy(r, phis, pos=self.position)
        self.add_part(self.ax.plot(x, y, 'o', c='k')[0])

        self._putname_(self.position[0], self.position[1] - 1.5 * r)

        connection_points = []
        for i in range(len(x)-1):
            connection_points.append((x[i], y[i]))

        self.connection_points = connection_points