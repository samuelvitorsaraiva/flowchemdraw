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

        self.build()

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

        self.connection_points = [(x, y-0.53*size/2 - 0.1*size)]

        '''

        size = self.dimention
        x, y = self.position
        boxstyle = "round,pad=0.1,rounding_size=0.1"  # Style
        self.add_part(self.ax.plot([x - size / 2, x - size / 2], [y - size / 3, y + size / 3], color='k'))
        self.add_part(self.ax.plot([x - size / 2, x - size / 2], [y - size / 3, y + size / 3], color='k'))

        rounded_square = patches.FancyBboxPatch((x-size/2, y), size/50, size, boxstyle=boxstyle, edgecolor='k', facecolor='k')
        self.add_part(self.ax.add_patch(rounded_square))
        rounded_square = patches.FancyBboxPatch((x, y), size, size/50, boxstyle=boxstyle, edgecolor='k', facecolor='k')
        self.add_part(self.ax.add_patch(rounded_square))

        

        img = plt.imread('icons/syringe.png')
        imagebox = OffsetImage(img, alpha=0.5, zoom=0.1)
        ao = AnchoredOffsetbox('lower left', pad=0, borderpad=1, child=imagebox)
        self.ax.add_artist(ao)

        '''


