import numpy as np
from flowchemdraw.utils.drawclass import components
import matplotlib.patches as patches
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (OffsetImage, TextArea, AnchoredOffsetbox, VPacker)
from PIL import Image

class syringe(components):

    type_object = 'devices'

    def __init__(self, ax: Figure, pos: (float, float) = (0.5, 0.5), name: str = 'syringe'):

        super().__init__(ax=ax, position=pos, type_object=syringe.type_object, name=name, parent=self)

        self.settup_connections()

        self.build()

    def settup_connections(self):
        size = self.dimention * 2
        x, y = self.position
        self.connection_points = {1: {'name': None, 'pairs': [1], 'position': (x, y-0.53*size/2 - 0.1*size)}}

    def build(self):

        size = self.dimention * 2
        x, y = self.position

        # Barrel
        barrel = patches.Rectangle((x-0.1*size/2, y-0.5*size/2), 0.1*size, 0.5*size, linewidth=1, edgecolor='black', facecolor='white')
        self.add_part(self.ax.add_patch(barrel))

        # Plunger
        plunger = patches.Rectangle((x-0.1*size/2, y-0.15*size/2), 0.1*size, 0.15*size, linewidth=1, edgecolor='black', facecolor='black', alpha=0.5)
        self.add_part(self.ax.add_patch(plunger))

        # Plunger rod
        plunger_rod = patches.Rectangle((x-0.02*size/2, y+0.15*size/2), 0.02*size, 0.3*size, linewidth=1, edgecolor='black', facecolor='black', alpha=0.5)
        self.add_part(self.ax.add_patch(plunger_rod))

        # Needle

        # needle = patches.FancyArrow(0.35, 0.2, 0, -0.1, width=0.01, head_width=0.03, head_length=0.02, linewidth=1, edgecolor='black', facecolor='black')
        # ax.add_patch(needle)
        barrel = patches.Rectangle((x-0.05*size/2, y-0.53*size/2), 0.05*size, 0.03*size, linewidth=1, edgecolor='black', facecolor='k')
        self.add_part(self.ax.add_patch(barrel))

        self.add_part(self.ax.plot([x] * 2, [y-0.53*size/2, y-0.53*size/2 - 0.1*size], color='black')[0])

        # Additional details like marks on the barrel
        Y_MIN = y - 0.5*size/2
        for i in range(6):
            self.add_part(self.ax.plot([x-0.1*size/2, x], [Y_MIN + i * 0.08 * size, Y_MIN + i * 0.08 * size], color='black')[0])

        #self.add_part(self.ax.plot(x, y-0.53*size/2 - 0.1*size, 'o', color='red'))

        self._putname_(x, y, where='above')

        self.arrow_information = False

    def operation_set(self, direction='right'):

        if self.arrow_information:

            self.parts[-1].remove()

            self.arrow_information = False

        else:

            size = self.dimention * 2

            pos = self.position

            if direction == 'right':
                xy = (pos[0] + size / 4, pos[1] + size / 3)
                xytext = (pos[0] + size / 4, pos[1] - size / 3)
            else:
                xytext = (pos[0] + size / 4, pos[1] + size / 3)
                xy = (pos[0] + size / 4, pos[1] - size / 3)

            arrow = self.ax.annotate('', xy=xy, xytext=xytext,
                        arrowprops={'arrowstyle': '-|>'}, va='center')

            self.add_part(arrow)

            self.arrow_information = True



