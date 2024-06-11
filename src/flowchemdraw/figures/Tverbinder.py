import numpy as np
from flowchemdraw.utils.drawclass import components
from matplotlib.figure import Figure
import matplotlib.patches as patches

class Tverbinder(components):

    type_object = 'others'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'Tverbinder'):

        super().__init__(ax=ax, position=pos, type_object=Tverbinder.type_object, name=name, parent=self)

        self.build()


    def build(self):

        r = self.dimention / 1.2

        pos = self.position

        square = patches.Rectangle((pos[0], pos[1] - r / 2), r / 10, r, edgecolor='black', facecolor='black', alpha=1)
        self.add_part(self.ax.add_patch(square))
        square = patches.Rectangle((pos[0], pos[1]), r/1.5, r / 10, edgecolor='black', facecolor='black', alpha=1)
        self.add_part(self.ax.add_patch(square))

        self.connection_points = [(pos[0] + r/20, pos[1] + r/2),
                                  (pos[0] + r/20, pos[1] - r/2),
                                  (pos[0] + r/1.5, pos[1] +  r / 20)]

        #self._putname_(pos[0], pos[1] - 0.75 * r)