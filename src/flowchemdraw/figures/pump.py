import numpy as np
from flowchemdraw.utils.drawclass import components
from flowchemdraw.utils import math

PATTERN_DIMENSION = 1
class pump(components):

    def __init__(self, ax, pos=(0.5, 0.5)):
        super().__init__(ax=ax, position=pos, parent=self)

        self.build()

    def build(self):
        phis = np.arange(0, 6.28, 0.01)
        r = PATTERN_DIMENSION / 2
        self.add_part(self.ax.plot(*math.xy(r, phis, pos=self.position), c='k', ls='-')[0])
        self.add_part(
            self.ax.plot([self.position[0], self.position[0] + r], [self.position[1] - r, self.position[1]], color='k')[0])
        self.add_part(
            self.ax.plot([self.position[0], self.position[0] + r], [self.position[1] + r, self.position[1]], color='k')[0])

        self.connection_points = [(self.position[0] - r, self.position[1]), (self.position[0] + r, self.position[1])]