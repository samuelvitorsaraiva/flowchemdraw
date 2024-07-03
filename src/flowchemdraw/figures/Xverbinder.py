import numpy as np
from flowchemdraw.utils.drawclass import components
from matplotlib.figure import Figure
import matplotlib.patches as patches

class Xverbinder(components):

    type_object = 'others'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'Xverbinder'):

        super().__init__(ax=ax, position=pos, type_object=Xverbinder.type_object, name=name, parent=self)

        self.settup_connections()

        self.build()

    def settup_connections(self):
        r = self.dimention / 1.2
        pos = self.position

        self.connection_points = {1: {'name': None, 'pairs': [2, 3, 4], 'position': (pos[0] + r/20, pos[1] + r/2)},
                                  2: {'name': None, 'pairs': [1, 3, 4], 'position': (pos[0] + r/20, pos[1] - r/2)},
                                  3: {'name': None, 'pairs': [1, 2, 4], 'position': (pos[0] + r/1.5, pos[1] + r / 20)},
                                  4: {'name': None, 'pairs': [1, 2, 3], 'position': (pos[0] - r/1.5, pos[1] + r / 20)}}

    def build(self):

        r = self.dimention / 1.2

        pos = self.position

        square = patches.Rectangle((pos[0], pos[1] - r / 2), r / 10, r, edgecolor='black', facecolor='black', alpha=1)
        self.add_part(self.ax.add_patch(square))
        square = patches.Rectangle((pos[0] - r / 1.5, pos[1]), 4 * r / 3, r / 10, edgecolor='black', facecolor='black', alpha=1)
        self.add_part(self.ax.add_patch(square))

        #self._putname_(pos[0], pos[1] - 0.75 * r)