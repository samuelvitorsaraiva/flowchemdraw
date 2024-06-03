import numpy as np
from flowchemdraw.utils.drawclass import components
import matplotlib.patches as patches
from matplotlib.figure import Figure

class syringe(components):

    type_object = 'devices'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'syringe'):

        super().__init__(ax=ax, position=pos, type_object=syringe.type_object, name=name, parent=self)

        self.build()

    def build(self):

        size = self.dimention
        x, y = self.position
        boxstyle = "round,pad=0.1,rounding_size=0.1"  # Style
        rounded_square = patches.FancyBboxPatch((x, y), size, size, boxstyle=boxstyle, edgecolor='k', facecolor='none')
        self.add_part(self.ax.add_patch(rounded_square))


        self._putname_(self.position[0] + size / 2, self.position[1] - size / 5)

        self.connection_points = [(self.position[0] - size/2, self.position[1])]