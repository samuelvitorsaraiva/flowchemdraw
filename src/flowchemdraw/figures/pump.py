import numpy as np
from flowchemdraw.utils.drawclass import components
from flowchemdraw.utils import math
from matplotlib.figure import Figure

class pump(components):

    type_object = 'devices'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'pump'):

        super().__init__(ax=ax, position=pos, type_object=pump.type_object, name=name, parent=self)

        self.settup_connections()

        self.build()

    def settup_connections(self):
        r = self.dimention / 2
        self.connection_points = {1: {'name': None, 'pairs': [2], 'position': (self.position[0] - r, self.position[1])},
                                  2: {'name': None, 'pairs': [1], 'position': (self.position[0] + r, self.position[1])}}

    def build(self):
        phis = np.arange(0, 6.28, 0.01)
        r = self.dimention / 2
        self.add_part(self.ax.plot(*math.xy(r, phis, pos=self.position), c='k', ls='-')[0])
        self.add_part(
            self.ax.plot([self.position[0], self.position[0] + r], [self.position[1] - r, self.position[1]], color='k')[0])
        self.add_part(
            self.ax.plot([self.position[0], self.position[0] + r], [self.position[1] + r, self.position[1]], color='k')[0])

        self._putname_(self.position[0], self.position[1] - 1.5 * r)

        self.operation_theta = 0

    def operation_set(self, **kwargs):

        if True:

            if self.operation_part:

                for item in self.operation_part:

                    item.remove()

                self.operation_part = []

            pos = self.position

            size = self.dimention * 2

            if kwargs['direction'] == 1:

                direction = 90

                x, y = pos[0], pos[1] - size/7

                increase = -1

            else:

                direction = -90

                x, y = pos[0], pos[1] + size / 7

                increase = 1

            self.operation_theta += increase

            if abs(self.operation_theta) > 350:

                self.operation_theta = increase



            [arc, arrow] = math.circarrowdraw(x,
                                              y,
                                              radius=size/7,
                                              aspect=1,
                                              direction=direction,
                                              closingangle=self.operation_theta,
                                              arrowheadrelativesize=0.3, arrowheadopenangle=30)

            self.operation_part.append(self.ax.plot(arc[0], arc[1], c='k', ls='-')[0])

            self.operation_part.append(self.ax.plot(arrow[0], arrow[1], c='k', ls='-')[0])

            self.arrow_information = True

